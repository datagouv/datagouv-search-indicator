<template>
<div>
  <b-tabs justified>
    <!-- Add your b-tab components here -->
    <template slot="tabs-end">
      <b-nav-item v-for="m in models" :key="m.name"
        :active="m.name == model.name"
        @click="setModel(m)">
        {{ m.plural }} <b-badge>{{ queryCounter[m.name] }}</b-badge>
      </b-nav-item>
    </template>
  </b-tabs>
  <b-table striped outlined hover show-empty
      :items="queries" :fields="fields" @row-clicked="display"
      empty-text="Aucune requête"
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
</div>
</template>

<script>
import {mapState, mapGetters, mapActions} from 'vuex'
import ParamsList from '../query/param-list.vue'
import models from '../models'

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
      models,
    }
  },
  computed: {
    items() {
      return this.details.queries.filter(query => query.model == this.model.name)
    },
    ...mapState(['toc', 'domain', 'details', 'config', 'model']),
    ...mapGetters(['queries', 'queryCounter']),
  },
  methods: {
    display(item) {
      this.$router.push({
        name: 'query',
        params: {
          domain: this.domain,
          date: this.details.date,
          query: item.uid
        }
      })
    },
    rowClass(query, type) {
      if (!query) return
      const classes = ['clickable']
      if (!query.found) {
        classes.push('table-danger')
      } else {
        classes.push(query.rank > this.config.minRank ? 'table-warning': 'table-success')
      }
      return classes
    },
    ...mapActions(['setModel']),
  }
}
</script>

<style scoped>
table.table, table.table >>> thead th { border-top: none !important }
</style>
