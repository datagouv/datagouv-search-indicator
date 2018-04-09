<template>
 <b-table striped outlined hover
    :items="toc" :fields="fields" @row-clicked="display"
    tbody-tr-class="clickable">
  <template slot="date" slot-scope="data">
    {{ data.item.date | datetime }}
  </template>
</b-table>
</template>

<script>
import {format, parse} from 'date-fns'
import {mapGetters} from 'vuex'

export default {
  data() {
    return {
      fields: [
        { label: 'Date', key: 'date' },
        { label: 'Queries', key: 'total' },
        { label: 'Found', key: 'found' },
        { label: 'Average rank', key: 'avg_rank' },
        { label: 'score', key: 'score' },
      ],
    }
  },
  computed: {
    ...mapGetters(['toc', 'domain'])
  },
  methods: {
    display(item) {
      this.$router.push({name: 'run', params: {domain: this.domain, date: item.date}})
    }
  }
}
</script>

<style>
</style>
