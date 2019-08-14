# datagouv-search-indicator

[![Build Status](https://travis-ci.org/etalab/datagouv-search-indicator.svg?branch=master)](https://travis-ci.org/etalab/datagouv-search-indicator)

Keep track of udata search results accross time and generate a static site to explore them.

## Contributing queries

Queries are stored in:
- [`data/datasets.csv`](data/datasets.csv) for Dataset search
- [`data/organizations.csv`](data/organizations.csv) for Organizations search

These CSVs have the same 3-columns format:
- `query`: a pure text search query (ie. `q` parameter)
- `params`: a search querystring (ie. `tag=something&tag=other`)
- `expected`: the expected model identifier

At least one of `query` and `params` is mandatory. If you have a `q` parameter in `params` and a `query`, the `q` parameter will be overwritten by `query`.


## Running benchmark

Requires Python 3.6+

``` bash
pip install -r requirements.pip
inv run -d my.domain.com
```

## Frontend Setup

Use Node 9.4.0 (`nvm install/nvm use` if you have nvm installed)

``` bash
# install dependencies
npm install

# serve with hot reload at localhost:8080
npm run dev

# build for production with minification
npm run build
```
