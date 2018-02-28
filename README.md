# datagouv-search-indicator

[![Build Status](https://travis-ci.org/etalab/datagouv-search-indicator.svg?branch=master)](https://travis-ci.org/etalab/datagouv-search-indicator)

Keep track of udata search results accross time and generate a static site to explore them.


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
