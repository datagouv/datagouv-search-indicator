<template>
 <b-table striped outlined hover
    :items="toc" :fields="fields" @row-clicked="display"
    tbody-tr-class="clickable">
  <template slot="date" slot-scope="data">
    {{ data.item.date | datetime }}
  </template>
  <template slot="coverage" slot-scope="data">
      <b-progress :max="data.item.total" show-value>
           <b-progress-bar :value="data.item.found" variant="success"></b-progress-bar>
           <b-progress-bar :value="data.item.below" variant="warning"></b-progress-bar>
           <b-progress-bar :value="data.item.total - data.item.found" variant="danger"></b-progress-bar>
      </b-progress>
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
        { label: 'Coverage', key: 'coverage'},
        { label: 'Average rank', key: 'avg_rank' },
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
