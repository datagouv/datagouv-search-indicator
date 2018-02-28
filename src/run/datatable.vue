<template>
<v-layout column align-center>
  <v-data-table :headers="headers" :items="details.queries" hide-actions class="elevation-1">
    <template slot="items" slot-scope="props">
      <tr @click="display(props.item)">
        <td>{{ props.item.query }}</td>
        <td class="text-xs-right">{{ props.item.title }}</td>
        <td class="text-xs-right">{{ props.item.found }}</td>
        <td class="text-xs-right">{{ props.item.rank }}</td>
        <td class="text-xs-right">{{ props.item.page }}</td>
        <td class="text-xs-right">{{ props.item.total }}</td>
      </tr>
    </template>
  </v-data-table>
</v-layout>
</template>

<script>
import {mapGetters} from 'vuex'

export default {
  data() {
    return {
      headers: [
        { text: 'Query', value: 'query', align: 'left' },
        { text: 'Expected', value: 'title' },
        { text: 'Found', value: 'found' },
        { text: 'Rank', value: 'rank' },
        { text: 'Page', value: 'page' },
        { text: 'Total', value: 'total' },
      ],
    }
  },
  computed: {
    ...mapGetters(['toc', 'domain', 'details'])
  },
  methods: {
    display(item) {
      this.$router.push({name: 'query', params: {domain: this.domain, date: this.details.date, query: item.query}})
    }
  }
}
</script>

<style>

</style>
