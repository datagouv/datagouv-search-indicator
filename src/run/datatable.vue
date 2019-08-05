<template>
 <b-table striped outlined hover
    :items="details.queries" :fields="fields" @row-clicked="display"
    :tbody-tr-class="rowClass">
  <template slot="query" slot-scope="data">
    {{ data.item.query }}
    <params-list :params="data.item.params"></params-list>
  </template>
  <template slot="found" slot-scope="data">
    <font-awesome-icon v-if="data.item.found" icon="check" />
    <font-awesome-icon v-else icon="times" />
  </template>
  <template slot="rank" slot-scope="data">
    <span v-if="data.item.found">{{ data.item.rank }}</span>
    <font-awesome-icon v-else icon="times" />
  </template>
  <template slot="page" slot-scope="data">
    <span v-if="!data.item.error">{{ data.item.page }}</span>
    <font-awesome-icon v-else icon="times" />
  </template>
  <template slot="total" slot-scope="data">
    <span v-if="!data.item.error">{{ data.item.total }}</span>
    <font-awesome-icon v-else icon="times" />
  </template>
</b-table>
</template>

<script>
import {mapState} from 'vuex'
import ParamsList from '../query/param-list.vue'

export default {
  name: 'run-datatable',
  components: {ParamsList},
  data() {
    return {
      fields: [
        { label: 'Query', key: 'query', sortable: true },
        { label: 'Expected', key: 'title', sortable: true },
        { label: 'Found', key: 'found', sortable: true, class: 'text-center f85'},
        { label: 'Rank', key: 'rank', sortable: true, class: 'text-center f85' },
        { label: 'Page', key: 'page', sortable: true, class: 'text-center f85' },
        { label: 'Total', key: 'total', sortable: true, class: 'text-center f85' },
      ],
    }
  },
  computed: {
    ...mapState(['toc', 'domain', 'details', 'config']),
  },
  methods: {
    display(item) {
      this.$router.push({
        name: 'query',
        params: {
          domain: this.domain,
          date: this.details.date,
          query: item.query
        }
      })
    },
    rowClass(query, type) {
      const classes = ['clickable']
      if (!query.found) {
        classes.push('table-danger')
      } else {
        classes.push(query.rank > this.config.minRank ? 'table-warning': 'table-success')
      }
      return classes
    }
  }
}
</script>

<style>

</style>
