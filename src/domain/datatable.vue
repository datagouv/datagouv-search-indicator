<template>
<v-layout column align-center>
  <v-data-table :headers="headers" :items="toc" hide-actions class="elevation-1">
    <template slot="items" slot-scope="props">
      <tr @click="display(props.item)">
        <td>{{ props.item.date | datetime }}</td>
        <td class="text-xs-right">{{ props.item.total }}</td>
        <td class="text-xs-right">{{ props.item.found }}</td>
        <td class="text-xs-right">{{ props.item.avg_rank }}</td>
        <td class="text-xs-right">{{ props.item.score }}</td>
      </tr>
    </template>
  </v-data-table>
</v-layout>
</template>

<script>
import {format, parse} from 'date-fns'
import {mapGetters} from 'vuex'

export default {
  data() {
    return {
      headers: [
        { text: 'Date', value: 'date', align: 'left' },
        { text: 'Queries', value: 'total' },
        { text: 'Found', value: 'found' },
        { text: 'Average rank', value: 'avg_rank' },
        { text: 'score', value: 'score' },
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
