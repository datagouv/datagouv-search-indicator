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
        { label: 'Query', key: 'query', sortable: true, class: 'align-middle' },
        { label: 'Expected', key: 'title', sortable: true },
        { label: 'Found', key: 'found', sortable: true, class: 'align-middle text-center' },
        { label: 'Rank', key: 'rank', sortable: true, class: 'align-middle text-right' },
        { label: 'Page', key: 'page', sortable: true, class: 'align-middle text-right' },
        { label: 'Total', key: 'total', sortable: true, class: 'align-middle text-right' },
      ],
    }
  },
  computed: {
    ...mapGetters(['toc', 'domain', 'details']),
    items() {
        return this.details.queries.map(query => {
            query._cellVariants = {
                rank: this.rankClass(query.rank),
                found: query.found ? 'success' : 'danger'
            }
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
    },
    rankClass(rank){

        var cl = ''

        if (rank > 0 && rank <= 3) {
            cl = 'success'
        } else if (rank) {
            cl = 'warning'
        }

        return cl
    }
  }
}
</script>

<style>

</style>
