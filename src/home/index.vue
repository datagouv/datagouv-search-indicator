<template>
<v-layout column align-center>
  <div v-for="domain in config.domains">
    <v-btn large :to="{name: 'domain', params: {domain}}">{{ domain }}</v-btn>
  </div>
</v-layout>
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
