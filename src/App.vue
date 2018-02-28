<template>
  <v-app>
    <v-toolbar fixed app>
      <v-toolbar-title v-text="config.title"></v-toolbar-title>
      <v-spacer></v-spacer>
      <v-select :items="config.domains" v-model="domain" label="Domain" single-line hide-details bottom></v-select>
    </v-toolbar>
    <v-content>
      <v-container fluid>
        <breadcrumb></breadcrumb>
        <v-slide-x-transition mode="out-in">
          <router-view></router-view>
        </v-slide-x-transition>
      </v-container>
    </v-content>
    <v-footer app>
      <span>&copy; 2017</span>
    </v-footer>
  </v-app>
</template>

<script>
import {mapGetters, mapActions} from 'vuex'
import Breadcrumb from './components/breadcrumb.vue'

export default {
  components: {Breadcrumb},
  computed: {
    domain: {
      get() {
        return this.$store.getters.domain
      },
      set(value) {
        this.$router.push({name: 'domain', params: {domain: value}})
      }
    },
    ...mapGetters(['config'])
  },
  methods: {
    ...mapActions(['setDomain'])
  }
}
</script>
