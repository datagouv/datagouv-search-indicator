import Vue from 'vue'
import Vuex from 'vuex'
import { format } from 'date-fns'

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
  currentDate: state => state.run ? format(new Date(state.run.date), 'DD/MM/YYYY HH:mm') : undefined,
  currentQuery: state => state.query ? state.query.query : undefined,
  getDataset: state => id => state.datasets.find(row => row.id == id),
  oembedApi: state => state.details ? `${state.details.server}/api/1/oembed` : undefined,
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
    async getToc({ commit, state }) {
        try {
            commit('loading', true)
            const response = await getData(`${state.domain}/toc.json`)
            commit('toc', response)
            commit('loading', false)
        } catch (error) {
            console.error(error)
        }
    },
    async setRun({ commit, dispatch, state }, date) {
        const run = state.toc.find(row => row.date === date)
        commit('run', run)
        await dispatch('getDetails')
    },
    async getDetails({ commit, state }) {
        try {
            commit('loading', true)
            const response = await getData(
                `${state.domain}/${state.run.file}`
            )
            commit('details', response)
            commit('loading', false)
        } catch (error) {
            console.error(error)
        }
    },
    async setQuery({ commit, state }, uid) {
        try {
            const q = state.details.queries.find(row => row.uid == uid )
            commit('query', q)
            commit('dataset', undefined);
        } catch (error) {
            console.error(error)
        }
    },
    async getDataset({ commit, getters, state }, id) {
        try {
            if (!getters.getDataset(id)) {
                commit('loading', true)
                const dataset = await getData(
                    `${state.domain}/${
                        state.run.dirname
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
