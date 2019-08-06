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

import { library } from '@fortawesome/fontawesome-svg-core'
import {
  faCheck, faSearch, faSpinner, faStar, faTimes, faTag, faCopyright, faBookmark,
  faCalendar, faMapMarker, faBullseye, faFile, faFileAlt, faRecycle, faEye,
  faArrowDown, faArrowUp, faExternalLinkAlt,
} from '@fortawesome/free-solid-svg-icons'
import { faBuilding as farBuilding, faFile as farFile } from '@fortawesome/free-regular-svg-icons'
import {FontAwesomeIcon} from '@fortawesome/vue-fontawesome'

library.add(
  faCheck, faSearch, faSpinner, faStar, faTimes, faTag, faCopyright, faBookmark,
  faCalendar, faMapMarker, faBullseye, faFile, faFileAlt, faRecycle, faEye,
  faArrowDown, faArrowUp, faExternalLinkAlt,
  farBuilding, farFile
)


Vue.config.devtools = true
Vue.use(BootstrapVue);
Vue.use(Filters)
Vue.use(TreeView)
Vue.component('font-awesome-icon', FontAwesomeIcon)

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
