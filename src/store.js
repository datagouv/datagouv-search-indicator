import Vue from 'vue'
import Vuex from 'vuex'
import { format } from 'date-fns'
import models from './models'

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
    model: models[0],
    query: undefined,
    item: undefined,
    items: undefined,
}

const getters = {
  currentDate: state => state.run ? format(new Date(state.run.date), 'DD/MM/YYYY HH:mm') : undefined,
  currentQuery: state => state.query ? state.query.query : undefined,
  queries: state => state.details ? state.details.queries.filter(query => query.model == state.model.name): undefined,
  queryCounter: state => state.details ? state.details.queries.reduce((result, query) => {
    if (!result.hasOwnProperty(query.model)) {
      result[query.model] = 1
    } else {
      result[query.model]++
    }
    return result
  }, {}) : undefined,
  getItem: state => id => state.items.find(item => item.id == id),
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
    model(state, value) {
        state.model = value
    },
    query(state, value) {
        state.query = value
        state.items = []
    },
    item(state, value) {
        state.item = value
    },
    addItem(state, value) {
        state.items.push(value)
    },
    items(state, value) {
        state.items = value
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
    async setModel({ commit }, model) {
      commit('model', model)
    },
    async setQuery({ commit, state }, uid) {
        try {
            const q = state.details.queries.find(row => row.uid == uid )
            const model = models.find(model => model.name == q.model)
            commit('model', model)
            commit('query', q)
            commit('item', undefined);
        } catch (error) {
            console.error(error)
        }
    },
    async getItem({ commit, getters, state }, id) {
        try {
            if (!getters.getItem(id)) {
                commit('loading', true)
                const item = await getData(
                    `${state.domain}/${state.run.dirname}/${state.model.path}/${id}.json`
                )
                commit('addItem', item)
                commit('loading', false)
            }
        } catch (error) {
            console.error(error)
        }
    },
    async setItem({ commit, dispatch, getters }, id) {
        try {
            await dispatch('getItem', id)
            commit('item', getters.getItem(id))
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
