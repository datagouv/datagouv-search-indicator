<template>
<div>
  <v-card class="mb-5">
    <v-container fluid>
      <v-layout row wrap>
        <v-flex xs12 class="mb-1">
          <v-text-field prepend-icon="search" :value="query.query" hide-details single-line></v-text-field>
        </v-flex>
        <v-flex xs12 md10 offset-md1 lg8 offset-lg2>
          <o-embed :url="datasetUrl(query.expected)"></o-embed>
        </v-flex>
      </v-layout>
    </v-container>
  </v-card>
  <v-data-table
    :items="query.datasets"
    item-key="id"
    :headers="headers"
    :hide-headers="!query.datasets.length"
    hide-actions
    class="elevation-1"
  >
    <template slot="headers" slot-scope="props">
      <tr>
        <th colspan="3">
          <p v-if="query.found" class="text-xs-center subheading">
            Jeu de données trouvé parmi {{ query.total }} resultats
          </p>
          <p v-if="!query.found" class="text-xs-center subheading">
            Jeu de données non trouvé parmi {{ query.total }} resultats
          </p>
        </th>
      </tr>
    </template>
    <template slot="items" slot-scope="props">
      <tr class="clickable" :active="dataset ? props.item.id === dataset.id : false"
          @click="props.expanded = !props.expanded">
        <td class="fixed">
          <v-icon v-if="props.item.id === query.expected" color="amber">star</v-icon>
        </td>
        <td class="fixed">{{ props.index }}</td>
        <td>{{ props.item.title }}</td>
      </tr>
    </template>
    <template slot="no-data">
      <v-alert :value="true" color="error" icon="warning">Aucun résultat retourné</v-alert>
    </template>
    <template slot="expand" slot-scope="props">
      <dataset-details :dataset-id="props.item.id"></dataset-details>
    </template>
  </v-data-table>
</div>
</template>

<script>
import { mapGetters } from "vuex"
import OEmbed from '../components/oembed.vue'
import DatasetDetails from './dataset-details.vue'

export default {
  components: {OEmbed, DatasetDetails},
  computed: {
    ...mapGetters(['query', 'details'])
  },
  data() {
    return {
      dialog: false,
      treeViewOptions: {rootObjectKey: 'dataset', maxDepth: 0},
      headers: [
        { text: 'Attendu', sortable: false, width: '20px' },
        { text: 'Rank', align: 'left', width: '20px' },
        { text: 'Titre', align: 'left', value: 'title' },
      ],
    }
  },
  methods: {
    datasetUrl(id) {
      return `${this.details.server}/datasets/${id}/`
    }
  }
};
</script>

<style>
table.table {
  table-layout: fixed;
}

tr.clickable {
  cursor: pointer;
}

td.fixed {
  width: 20px;
}
</style>
