'''
These scripts are meant to build the data for the search result indicator dashboard.

It perform the following tasks:
- It parce a CSV file to perform search queries on data.gouv.fr,
 rank the expected results on data.gouv.fr

It makes use of the data.gouv.fr API wich returns the same result as the front end.


The expectected input file format is the following (column names matters):

| query                                           | expected                |
|-------------------------------------------------|-------------------------|
| The search query to submit to the search engine | The expected dataset id |


'''
import asyncio
import csv
import itertools
import httpx
import json
import os
import sys
import logging
import warnings

from datetime import datetime
from glob import glob
from invoke import task
from pathlib import Path
from progress.bar import ChargingBar

DEFAULT_DOMAIN = 'www.data.gouv.fr'
BASE_URL = 'https://www.data.gouv.fr/api/1/'
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
            self.error = str(e)
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

        # Domains
        self.dataset = DatasetAPI(self)
        self.org = OrganizationAPI(self)

    def url_for(self, path):
        return f'{self.scheme}://{self.domain}/api/1/{path}'

    async def get(self, path, **kwargs):
        url = self.url_for(path)
        timeout = kwargs.pop('timeout', self.timeout)
        result = await self.http.get(url, timeout=timeout, **kwargs)
        return result.json()


class DomainAPI:
    def __init__(self, api):
        self.api = api


class DatasetAPI(DomainAPI):
    async def get(self, id):
        return await self.api.get('datasets/{0}/'.format(id))

    async def search(self, query, page=1):
        params = {'q': query, 'page': page, 'page_size': PAGE_SIZE}
        return await self.api.get('datasets/', params=params)


class OrganizationAPI(DomainAPI):
    async def get(self, id):
        return await self.api.get('organizations/{0}/'.format(id))

    async def search(self, query, page=1):
        params = {'q': query, 'page': page, 'page_size': PAGE_SIZE}
        return await self.api.get('organizations/', params=params)


class QueryResult:
    found = False
    datasets = []
    rank = None
    total = 0
    page = None
    page_size = PAGE_SIZE
    error = None

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)


class Runner:
    def __init__(self, domain, max_pages=3, scheme='https', timeout=TIMEOUT, concurrency=CONCURRENCY):
        self.queue = asyncio.Queue()
        self.domain = domain
        self.scheme = scheme
        self.api = API(domain, scheme, timeout)
        self.max_pages = max_pages
        self.now = datetime.now()

        # Manage concurrency with an async Semaphore
        self.limiter = asyncio.Semaphore(concurrency)

    @property
    def timestamp(self):
        return self.now.isoformat(sep='-', timespec='minutes').replace(':', '-')

    @property
    def root(self):
        return Path('data') / self.domain / self.timestamp

    @property
    def datasets(self):
        return self.root / 'datasets'

    async def process(self):
        self.root.mkdir(parents=True, exist_ok=True)
        self.datasets.mkdir(parents=True, exist_ok=True)

        with open('data/queries.csv', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            bar = CompoundBar('Querying')
            for row in reader:
                bar.add_task(row['query'],
                             self.process_query(row['query'], row['expected']))

        results = await bar.wait()

        data = {
            'total': len(results),
            'found': count_found(results),
            'avg_rank': average_rank(results),
            'below': below(results),
            'score': score(results),
            'queries': results,
            'date': self.now.isoformat(timespec='seconds'),
            'server': '{scheme}://{domain}'.format(**self.__dict__)
        }

        outfile = self.root / 'queries.json'
        with outfile.open('w', encoding='utf-8') as jsonfile:
            json.dump(data, jsonfile, ensure_ascii=False)

        return results

    async def get_dataset(self, id):
        dataset_file = self.datasets / '{0}.json'.format(id)
        if dataset_file.exists():
            with dataset_file.open(encoding='utf-8') as jsonfile:
                dataset = json.load(jsonfile)
        else:
            dataset = await self.api.dataset.get(id)
            with dataset_file.open('w', encoding='utf-8') as jsonfile:
                json.dump(dataset, jsonfile, ensure_ascii=False)

        return dataset

    async def process_query(self, query, expected):
        async with self.limiter:
            result = await self.rank_query(query, expected)
            dataset = await self.get_dataset(expected)
        return {
            'query': query,
            'expected': expected,
            'title': dataset['title'],
            'found': result.found,
            'total': result.total,
            'rank': result.rank,
            'page': result.page,
            'datasets': result.datasets,
        }

    async def rank_query(self, query, expected):
        datasets = []
        page = 1
        rank = 0
        while page <= self.max_pages:
            result = await self.api.dataset.search(query, page=page)
            if 'data' not in result:
                return QueryResult(error='Bad response format: {}'.format(result),
                                   page=page,
                                   datasets=datasets)
            for rank, dataset in enumerate(result['data'], rank + 1):
                dataset = await self.get_dataset(dataset['id'])
                datasets.append({'id': dataset['id'], 'title': dataset['title']})
                if dataset['id'] == expected:
                    return QueryResult(found=True,
                                       rank=rank,
                                       page=page,
                                       page_size=result['page_size'],
                                       datasets=datasets,
                                       total=result['total'])
            if not result.get('next_page'):
                return QueryResult(page=page,
                                   page_size=result['page_size'],
                                   datasets=datasets,
                                   total=result['total'])
            page += 1


def count_found(results):
    return sum(1 for r in results if r and r['found'])


def below(results):
    return len([1 for r in results if r['found'] and r['rank'] >= 3])


def average_rank(results):
    ranks = [r['rank'] for r in results if r['found']]
    return sum(ranks) / float(len(ranks))


def score(results):
    return 0


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
            'below': data['below'] if 'below' in data else 0,
            'avg_rank': data['avg_rank'],
            'score': data['score'],
        })
    toc.sort(key=lambda r: r['date'])
    with open('data/{0}/toc.json'.format(domain), 'w', encoding='utf-8') as jsonfile:
        json.dump(toc, jsonfile, sort_keys=True, indent=4, ensure_ascii=False)

    success('TOC built for {0}'.format(domain))


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
