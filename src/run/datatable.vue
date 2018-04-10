<template>
 <b-table striped outlined hover
    :items="items" :fields="fields" @row-clicked="display"
    tbody-tr-class="clickable">
  <template slot="found" slot-scope="data">
    <font-awesome-icon v-if="data.item.found" icon="check" />
    <font-awesome-icon v-else icon="times" />
  </template>
</b-table>
</template>

<script>
import {mapGetters} from 'vuex'
import FontAwesomeIcon from '@fortawesome/vue-fontawesome'

export default {
  components: {FontAwesomeIcon},
  data() {
    return {
      fields: [
        { label: 'Query', key: 'query', sortable: true},
        { label: 'Expected', key: 'title', sortable: true },
        { label: 'Found', key: 'found', sortable: true },
        { label: 'Rank', key: 'rank', sortable: true },
        { label: 'Page', key: 'page', sortable: true },
        { label: 'Total', key: 'total', sortable: true },
      ],
    }
  },
  computed: {
    ...mapGetters(['toc', 'domain', 'details']),
    items() {
      return this.details.queries.map(query => {
        query._rowVariant = query.found ? 'success' : 'danger'
        return query
      })
    }
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
    }
  }
}
</script>

<style>

</style>
