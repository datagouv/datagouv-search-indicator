'''
These scripts are meant to build the data for the search result indicator dashboard.

It perform the following tasks:
- It parce a CSV file to perform search queries on a target udata instance,
- rank the expected results on the target udata instance
- store the query results details (including items payloads) as JSON files

It makes use of the udata API wich returns the same result as the front end.

The expected input format is a CSV file (one by model)
with the following columns (names matters):

- `query`: a text only search query to submit to the search engine
- `params`: a search querystring to submit to the search engine.
- `expected`: The expected item id

'''
import asyncio
import csv
import itertools
import httpx
import json
import os
import sys
import uuid
import warnings

from datetime import datetime
from glob import glob
from invoke import task
from pathlib import Path
from progress.bar import ChargingBar
from urllib.parse import parse_qs, urlencode

DEFAULT_DOMAIN = 'www.data.gouv.fr'
PAGE_SIZE = 20
TIMEOUT = 10
CONCURRENCY = 20


def color(code):
    '''A simple ANSI color wrapper factory'''
    return lambda t: '\033[{0}{1}\033[0;m'.format(code, t)


green = color('1;32m')
red = color('1;31m')
cyan = color('1;36m')
white = color('1;39m')
yellow = color('1;33m')


def header(text, *args, **kwargs):
    '''Display an header'''
    text = text.format(*args, **kwargs)
    print(' '.join((yellow('★'), white(text), yellow('★'))))
    sys.stdout.flush()


def info(text, *args, **kwargs):
    '''Display informations'''
    text = text.format(*args, **kwargs)
    print(' '.join((cyan('➤'), text)))
    sys.stdout.flush()


def success(text, *args, **kwargs):
    '''Display a success message'''
    text = text.format(*args, **kwargs)
    print(' '.join((green('✔'), white(text))))
    sys.stdout.flush()


def error(text, *args, **kwargs):
    '''Display an error message'''
    text = text.format(*args, **kwargs)
    print(' '.join((red('✘'), yellow(text))))
    sys.stdout.flush()


class CompoundBar(ChargingBar):
    suffix = '%(percent)d%% [%(index)d/%(max)d] (%(elapsed)ds)'

    def __init__(self, *args, **kwargs):
        self.lines = 0
        self.max = 1
        self.index = 0
        self.tasks = []
        super().__init__(*args, **kwargs)

    # def __enter__(self):

    def up(self):
        sys.stdout.write('\x1b[1A')
        sys.stdout.flush()
        self.lines -= 1

    def down(self):
        sys.stdout.write('\n')
        sys.stdout.flush()
        self.lines += 1

    def top(self):
        while self.lines > 0:
            self.up()

    def update(self):
        self.top()
        self.max = len(self.tasks)
        self.index = sum(1 for t in self.tasks if t.done)
        super().update()
        for t in self.tasks:
            self.down()
            self.writeln(t.spin())

    def add_task(self, label, coro):
        self.tasks.append(Spinner(label, coro))
        self.update()

    async def wait(self):
        while not all(t.done for t in self.tasks):
            self.update()
            await asyncio.sleep(0.1)
        self.update()
        self.finish()
        return self.results

    @property
    def results(self):
        return [t.result for t in self.tasks]


class Spinner:
    FRAMES = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']

    def __init__(self, label, coro):
        self.label = label
        self.done = False
        self.result = None
        self.error = None
        self.frames = itertools.cycle(self.FRAMES)
        self.spin()

        loop = asyncio.get_event_loop()
        self.task = loop.create_task(coro)
        self.task.add_done_callback(self.on_done)

    def spin(self):
        if self.done:
            self.picto = green('✔') if self.ok else red('✘')
        else:
            self.picto = cyan(next(self.frames))
        return self

    def __str__(self):
        if self.error:
            return '{0.picto} {0.label} ({0.error})'.format(self)
        return '{0.picto} {0.label}'.format(self)

    def on_done(self, future):
        try:
            self.result = future.result()
        except Exception as e:
            self.ok = False
            self.error = (str(e) or str(e.__class__.__name__)).split('\n')[0]
            self.result = {}
        else:
            self.ok = self.result['found']
        self.done = True
        self.spin()


class API:
    def __init__(self, domain, scheme='http', timeout=TIMEOUT):
        self.domain = domain
        self.scheme = scheme
        self.timeout = timeout
        self.http = httpx.AsyncClient()

    def url_for(self, path, **params):
        qs = urlencode(params, doseq=True)
        if qs:
            return f'{self.scheme}://{self.domain}/api/2/{path}search/?{qs}'
        return f'{self.scheme}://{self.domain}/api/1/{path}'

    async def get(self, path, **kwargs):
        url = self.url_for(path, **kwargs.pop('params', {}))
        timeout = kwargs.pop('timeout', self.timeout)
        result = await self.http.get(url, timeout=timeout, **kwargs)
        result.raise_for_status()
        return result.json()


class QueryResult:
    found = False
    items = []
    rank = None
    total = 0
    page = None
    page_size = PAGE_SIZE
    error = None
    uid = None

    def __init__(self, **kwargs):
        self.uid = str(uuid.uuid4())
        for key, value in kwargs.items():
            setattr(self, key, value)


def row_label(row):
    if row['query'] and row['params']:
        return '{query} ({params})'
    elif row['query']:
        return row['query']
    else:
        return row['params']


class Runner:
    def __init__(self, domain, max_pages=3, scheme='https', timeout=TIMEOUT,
                 concurrency=CONCURRENCY):
        self.domain = domain
        self.scheme = scheme
        self.api = API(domain, scheme, timeout)
        self.max_pages = max_pages
        self.now = datetime.now()
        self.concurrency = concurrency
        self.runners = [DatasetRunner(self), OrgRunner(self)]

    @property
    def timestamp(self):
        return self.now.isoformat(sep='-', timespec='minutes').replace(':', '-')

    @property
    def root(self):
        return Path('data') / self.domain / self.timestamp

    async def process(self):
        self.root.mkdir(parents=True, exist_ok=True)

        results = []

        for runner in self.runners:
            results.extend(await runner.process())

        data = compile_results('{scheme}://{domain}'.format(**self.__dict__), self.now, results)

        outfile = self.root / 'queries.json'
        with outfile.open('w', encoding='utf-8') as jsonfile:
            json.dump(data, jsonfile, ensure_ascii=False)

        return results


class ModelRunnner:
    model = None
    basename = None
    api_class = None

    def __init__(self, runner):
        self.runner = runner
        # Manage concurrency with an async Semaphore
        self.limiter = asyncio.Semaphore(runner.concurrency)

    @property
    def api(self):
        return self.runner.api

    @property
    def files(self):
        return self.runner.root / self.basename

    async def process(self):
        self.files.mkdir(parents=True, exist_ok=True)

        with open(f'data/{self.basename}.csv', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            bar = CompoundBar(f'Querying {self.basename}')
            for row in reader:
                bar.add_task(row_label(row),
                             self.process_query(row['query'], row['params'], row['expected']))

        return await bar.wait()

    async def get_item(self, id):
        item_file = self.files / f'{id}.json'
        if item_file.exists():
            with item_file.open(encoding='utf-8') as jsonfile:
                item = json.load(jsonfile)
        else:
            item = await self.get(id)
            with item_file.open('w', encoding='utf-8') as jsonfile:
                json.dump(item, jsonfile, ensure_ascii=False)

        return item

    async def process_query(self, query, params, expected):
        params = parse_qs(params)
        async with self.limiter:
            try:
                item = await self.get_item(expected)
            except httpx.exceptions.HttpError as e:
                item = {'title': f'{self.model}({expected}) injoignable'}
                result = QueryResult(error=f'Impossible de récupérer {self.model}:\n{e}',
                                     found=False)
            except Exception as e:
                item = {'title': f'{self.model}({expected}) injoignable'}
                result = QueryResult(error=f'Erreur inconnue:\n{e}',
                                     found=False)
            else:
                result = await self.rank_query(query, params, expected)

        return {
            'uid': result.uid,
            'query': query,
            'params': params,
            'expected': expected,
            'model': self.model,
            'title': item.get('title', item.get('name')),
            'found': result.found,
            'total': result.total,
            'rank': result.rank,
            'page': result.page,
            'items': result.items,
            'error': result.error,
        }

    async def rank_query(self, query, params, expected):
        items = []
        page = 1
        rank = 0
        while page <= self.runner.max_pages:
            result = await self.search(query, params, page=page)
            if 'data' not in result:
                return QueryResult(error=f'Mauvais format de réponse:\n{result}',
                                   page=page,
                                   items=items)
            for rank, item in enumerate(result['data'], rank + 1):
                item = await self.get_item(item['id'])
                items.append({'id': item['id'], 'title': item.get('title', item.get('name'))})
                if item['id'] == expected:
                    return QueryResult(found=True,
                                       rank=rank,
                                       page=page,
                                       page_size=result['page_size'],
                                       items=items,
                                       total=result['total'])
            if not result.get('next_page'):
                return QueryResult(page=page,
                                   page_size=result['page_size'],
                                   items=items,
                                   total=result['total'])
            page += 1

    async def get(self, id):
        raise NotImplementedError()

    async def search(self, query, params, page=1):
        raise NotImplementedError()


class DatasetRunner(ModelRunnner):
    model = 'Dataset'
    basename = 'datasets'

    async def get(self, id):
        return await self.api.get('datasets/{0}/'.format(id))

    async def search(self, query, params, page=1):
        params = {'page': page, 'page_size': PAGE_SIZE, **params}
        if query:
            params['q'] = query
        return await self.api.get('datasets/', params=params)


class OrgRunner(ModelRunnner):
    model = 'Organization'
    basename = 'organizations'

    async def get(self, id):
        return await self.api.get('organizations/{0}/'.format(id))

    async def search(self, query, params, page=1):
        params = {'page': page, 'page_size': PAGE_SIZE, **params}
        if query:
            params['q'] = query
        return await self.api.get('organizations/', params=params)


def count_found(results):
    return sum(1 for r in results if r and r['found'])


def count_errors(results):
    return sum(1 for r in results if r and r.get('error'))


def average_rank(results):
    ranks = [r['rank'] for r in results if r and r['found']]
    return sum(ranks) / float(len(ranks))


def ranks(results):
    ranks = [r['rank'] if r and r['found'] else 0 for r in results]
    out = [0] * (max(ranks) + 1)
    for result in results:
        if result and result['found']:
            out[result['rank']] += 1
    return out


def score(results):
    return (average_rank(results) * count_found(results)) / len(results)


def compile_results(server, timestamp, results):
    return {
        'total': len(results),
        'found': count_found(results),
        'avg_rank': average_rank(results),
        'ranks': ranks(results),
        'errors': count_errors(results),
        'score': score(results),
        'queries': results,
        'date': timestamp.isoformat(timespec='seconds'),
        'server': server
    }


@task
def toc(ctx, domain=DEFAULT_DOMAIN):
    '''Build the table of content for the dashboard'''
    header('Building TOC for {0}', domain)
    base_path = os.path.join('data', domain)
    toc = []
    for filename in glob('data/{0}/*/queries.json'.format(domain)):
        dirname = os.path.dirname(filename.replace(base_path + '/', ''))
        with open(filename, encoding='utf-8') as jsonfile:
            data = json.load(jsonfile)

        toc.append({
            'file': filename.replace(base_path + '/', ''),
            'dirname': dirname,
            'date': data['date'],
            'total': data['total'],
            'found': data['found'],
            'ranks': data['ranks'],
            'avg_rank': data['avg_rank'],
            'score': data['score'],
        })
    toc.sort(key=lambda r: r['date'])
    with open('data/{0}/toc.json'.format(domain), 'w', encoding='utf-8') as jsonfile:
        json.dump(toc, jsonfile, sort_keys=True, indent=4, ensure_ascii=False)

    success('TOC built for {0}'.format(domain))


@task
def fix(ctx, domain=DEFAULT_DOMAIN):
    '''Rebuild queries and tocs on model changes (if possible)'''
    header('Fixing metadata')
    for filename in glob('data/{0}/*/queries.json'.format(domain)):
        info('Fixing {0}', filename)
        # dirname = os.path.dirname(filename.replace(base_path + '/', ''))
        with open(filename, encoding='utf-8') as jsonfile:
            data = json.load(jsonfile)

        server = data['server']
        timestamp = datetime.strptime(data['date'], '%Y-%m-%dT%H:%M:%S')
        fixed = compile_results(server, timestamp, data['queries'])

        with open(filename, 'w', encoding='utf-8') as jsonfile:
            json.dump(fixed, jsonfile, ensure_ascii=False)
        success('Fixed  {0}', filename)
    toc(ctx, domain)


@task
def event(ctx, label, domain=DEFAULT_DOMAIN):
    '''Insert a notable event in the timeline'''
    header('Insert event {0} for {1}', label, domain)
    filename = os.path.join('data', domain, 'events.json')
    with open(filename, encoding='utf-8') as jsonfile:
        data = json.load(jsonfile)
    data.append({
        'label': label,
        'date': datetime.now().isoformat(),
    })
    data.sort(key=lambda r: r['date'])
    with open(filename, 'w', encoding='utf-8') as jsonfile:
        json.dump(data, jsonfile, sort_keys=True, indent=4, ensure_ascii=False)
    success('Event inserted')


@task
def run(ctx, domain=DEFAULT_DOMAIN, max_pages=3, scheme='https', timeout=TIMEOUT,
        concurrency=CONCURRENCY, verbose=False):
    '''Run benchmarch on a given domain'''
    header('Running benchmark on {0}', domain)
    loop = asyncio.get_event_loop()
    # Report all mistakes managing asynchronous resources.
    if verbose:
        loop.set_debug(True)
        warnings.simplefilter('always', ResourceWarning)
    runner = Runner(domain, max_pages, scheme, timeout, concurrency)
    results = loop.run_until_complete(runner.process())
    loop.close()
    success('Benchmark run {0} queries on {1}', len(results), domain)
    toc(ctx, domain)
