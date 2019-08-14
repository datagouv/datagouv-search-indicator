<template>
<b-table striped outlined hover
    :items="toc" :fields="fields" @row-clicked="display"
    tbody-tr-class="clickable">
  <template slot="date" slot-scope="data">
    {{ data.item.date | datetime }}
  </template>
  <template slot="coverage" slot-scope="data">
    <b-progress :max="data.item.total" show-value>
      <b-progress-bar :value="data.item.found - below(data.item)" variant="success"></b-progress-bar>
      <b-progress-bar :value="below(data.item)" variant="warning"></b-progress-bar>
      <b-progress-bar :value="data.item.total - data.item.found" variant="danger"></b-progress-bar>
    </b-progress>
  </template>
</b-table>
</template>

<script>
import {format, parse} from 'date-fns'
import {mapState} from 'vuex'

export default {
  data() {
    return {
      fields: [
        { label: 'Date', key: 'date' },
        { label: 'Queries', key: 'total', class: 'text-center' },
        {
          label: 'Coverage',
          key: 'coverage',
          headerTitle: `Values are "top ranked/bad/not found"`,
        },
        {
          label: 'Average rank',
          headerTitle: 'Only includes matched queries. Lower is better',
          key: 'avg_rank',
          class: 'text-center',
          formatter: f => f.toFixed(2),
        },
        {
          label: 'Score',
          headerTitle: 'Includes all queries. Lower is better',
          key: 'score',
          class: 'text-center',
          formatter: f => f.toFixed(2)
        },
      ],
    }
  },
  computed: {
    ...mapState(['toc', 'domain', 'config'])
  },
  methods: {
    display(item) {
      this.$router.push({name: 'run', params: {domain: this.domain, date: item.date}})
    },
    below(item) {
      return item.ranks.slice(this.config.minRank + 1).reduce((total, count) => total + count, 0)
    }

  }
}
</script>

<style>
</style>
