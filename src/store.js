import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

const debug = process.env.NODE_ENV !== 'production'

async function getData(path) {
    const response = await fetch(`./data/${path}`)
    return await response.json()
}

const state = {
    loading: false,
    config: {},
    domain: undefined,
    toc: undefined,
    run: undefined,
    details: undefined,
    query: undefined,
    dataset: undefined,
    datasets: undefined,
}

const getters = {
  loading: state => state.loading,
  config: state => state.config,
  domain: state => state.domain,
  toc: state => state.toc,
  run: state => state.run,
  details: state => state.details,
  query: state => state.query,
  currentDate: state => new Date(state.run.date).toLocaleDateString(),
  currentQuery: state => state.query.query,
  getDataset: state => id => state.datasets.find(row => row.id == id),
  dataset: state => state.dataset,
  datasets: state => state.datasets,
  oembedApi: state => `${state.details.server}/api/1/oembed`,
  // oembedUrls: state => [
  //     `${state.domain}/datasets/*/`,
  //     `${state.domain}/*/datasets/*/`,
  //     `${state.domain}/reuses/*/`,
  //     `${state.domain}/*/reuses/*/`,
  // ],
};

const mutations = {
    loading(state, value) {
        state.loading = value
    },
    config(state, value) {
        state.config = value
    },
    domain(state, value) {
        state.domain = value
    },
    toc(state, value) {
        state.toc = value
    },
    run(state, value) {
        state.run = value
    },
    details(state, value) {
        state.details = value
    },
    query(state, value) {
        state.query = value
        state.datasets = []
    },
    dataset(state, value) {
        state.dataset = value
    },
    addDataset(state, value) {
        state.datasets.push(value)
    },
    datasets(state, value) {
        state.datasets = value
    }
}

const actions = {
    async getConfig({ commit }) {
        try {
            commit('loading', true)
            const response = await getData('config.json')
            commit('config', response)
            commit('loading', false)
        } catch (error) {
            console.error(error)
        }
    },
    async setDomain({ commit, dispatch }, domain) {
        commit('domain', domain)
        await dispatch('getToc')
    },
    async getToc({ commit, getters }) {
        try {
            commit('loading', true)
            const response = await getData(`${getters.domain}/toc.json`)
            commit('toc', response)
            commit('loading', false)
        } catch (error) {
            console.error(error)
        }
    },
    async setRun({ commit, dispatch, getters }, date) {
        const run = getters.toc.find(row => row.date === date)
        commit('run', run)
        await dispatch('getDetails')
    },
    async getDetails({ commit, getters }) {
        try {
            commit('loading', true)
            const response = await getData(
                `${getters.domain}/${getters.run.file}`
            )
            commit('details', response)
            commit('loading', false)
        } catch (error) {
            console.error(error)
        }
    },
    async setQuery({ commit, getters }, query) {
        try {
            const q = getters.details.queries.find(row => row.query == query)
            commit('query', q)
            commit('dataset', undefined);
        } catch (error) {
            console.error(error)
        }
    },
    async getDataset({ commit, getters }, id) {
        try {
            if (!getters.getDataset(id)) {
                commit('loading', true)
                const dataset = await getData(
                    `${getters.domain}/${
                        getters.run.dirname
                    }/datasets/${id}.json`
                )
                commit('addDataset', dataset)
                commit('loading', false)
            }
        } catch (error) {
            console.error(error)
        }
    },
    async setDataset({ commit, dispatch, getters }, id) {
        try {
            await dispatch('getDataset', id)
            commit('dataset', getters.getDataset(id))
        } catch (error) {
            console.error(error)
        }
    }
}


export default new Vuex.Store({
    actions,
    getters,
    mutations,
    state,

    strict: debug,
})
