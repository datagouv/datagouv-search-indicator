<template>
<div>
  <router-view></router-view>
</div>
</template>

<script>
import {mapActions} from 'vuex'

export default {
  /**
   * Fetch on domain change
   */
  beforeRouteUpdate (to, from, next) {
    this.setDomain(to.params.domain).then(next)
  },
  methods: {
    ...mapActions(['setDomain'])
  }
}
</script>

<style>

</style>
