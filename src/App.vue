<template>
<div>
  <b-navbar toggleable="md" type="dark" variant="info">
    <b-navbar-toggle target="nav_collapse"></b-navbar-toggle>

    <b-navbar-brand href="#">{{ config.title }}</b-navbar-brand>

    <b-collapse is-nav id="nav_collapse">

      <!-- Right aligned nav items -->
      <b-navbar-nav class="ml-auto">

        <b-nav-item-dropdown :text="domain" right>
          <b-dropdown-item v-for="dom in config.domains" :key="dom"
            :to="{name: 'domain', params: {domain: dom}}">
            {{ dom }}
          </b-dropdown-item>
        </b-nav-item-dropdown>
      </b-navbar-nav>
    </b-collapse>
  </b-navbar>

  <main>
    <b-container fuild>
      <breadcrumb class="mt-2"></breadcrumb>
      <router-view></router-view>
    </b-container>
  </main>
</div>
</template>

<script>
import {mapState, mapActions} from 'vuex'
import Breadcrumb from './components/breadcrumb.vue'

export default {
  name: 'app',
  components: {Breadcrumb},
  computed: {
    ...mapState(['config', 'domain'])
  }
}
</script>
