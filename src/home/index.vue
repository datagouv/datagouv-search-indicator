<template>
<b-row align-v="center" align-h="center">
  <b-col class="pb-2" cols="12" v-for="domain in config.domains" :key="domain" >
    <b-button block variant="primary" :to="{name: 'domain', params: {domain}}">{{ domain }}</b-button>
  </b-col>
</b-row>
</template>

<script>
import {mapGetters, mapActions} from 'vuex'

export default {
  computed: {
    ...mapGetters(['config'])
  }
}
</script>

<style>

</style>
