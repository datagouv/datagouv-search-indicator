import Vue from 'vue'
import App from './App.vue'
import TreeView from 'vue-json-tree-view'
import BootstrapVue from 'bootstrap-vue'

import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'
import './style.css'

import Filters from './plugins/filters'
import router from './router'
import store from './store'

import {mapGetters, mapActions} from 'vuex'

import fontawesome from '@fortawesome/fontawesome'
import { faSpinner, faStar, faCheck, faTimes } from '@fortawesome/fontawesome-free-solid'

fontawesome.library.add(faSpinner, faStar, faCheck, faTimes)

Vue.config.devtools = true
Vue.use(BootstrapVue);
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
