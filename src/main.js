import Vue from 'vue'
import App from './App.vue'
import Vuetify from 'vuetify'
import 'vuetify/dist/vuetify.css'
import TreeView from 'vue-json-tree-view'

import Filters from './plugins/filters'
import router from './router'
import store from './store'

import {mapGetters, mapActions} from 'vuex'

Vue.use(Vuetify)
Vue.use(Filters)
Vue.use(TreeView)

new Vue({
  el: '#app',
  router, store,
  render: h => h(App),
  created() {
    this.getConfig()
  },
  methods: {
    ...mapActions(['getConfig']),
  },
})
