<template>
 <b-table striped outlined hover
    :items="details.queries" :fields="fields" @row-clicked="display"
    tbody-tr-class="clickable">
</b-table>
</template>

<script>
import {mapGetters} from 'vuex'

export default {
  data() {
    return {
      fields: [
        { label: 'Query', key: 'query'},
        { label: 'Expected', key: 'title' },
        { label: 'Found', key: 'found' },
        { label: 'Rank', key: 'rank' },
        { label: 'Page', key: 'page' },
        { label: 'Total', key: 'total' },
      ],
    }
  },
  computed: {
    ...mapGetters(['toc', 'domain', 'details'])
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
