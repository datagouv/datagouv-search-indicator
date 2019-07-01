<template>
<div>
  <b-row>
    <b-col cols="12">
      <b-input-group class="mb-3">
        <b-input-group-prepend>
          <b-btn disabled variant="outline-primary">
            <font-awesome-icon icon="search" />
          </b-btn>
        </b-input-group-prepend>
        <b-form-input :value="query.query" />
      </b-input-group>
    </b-col>
  </b-row>
  <b-row align-h="center" class="mb-3">
    <b-col cols="12" md="10" lg="8">
      <o-embed :url="datasetUrl(query.expected)"></o-embed>
    </b-col>
  </b-row>
  <b-table striped outlined hover caption-top fixed class="result-table"
      :items="items" :fields="fields" @row-clicked="toggle"
      tbody-tr-class="clickable">
    <template slot="table-caption" v-if="query.found">
      Jeu de données trouvé parmi {{ query.total }} resultats
    </template>
    <template slot="table-caption" v-if="!query.found">
      Jeu de données non trouvé parmi {{ query.total }} resultats
    </template>
    <template slot="expected" slot-scope="data">
      <font-awesome-icon v-if="data.item.id === query.expected"
        icon="star" style="color: yellow"/>
    </template>
    <template slot="index" slot-scope="data">
      {{ data.index + 1 }}
    </template>
    <template slot="row-details" slot-scope="row">
      <dataset-details :dataset-id="row.item.id"></dataset-details>
    </template>
  </b-table>
</div>
</template>

<script>
import { mapState } from "vuex"
import OEmbed from '../components/oembed.vue'
import DatasetDetails from './dataset-details.vue'

export default {
  components: {OEmbed, DatasetDetails},
  computed: {
    ...mapState(['query', 'details']),
    items() {
      return this.query.datasets.map(dataset => {
        dataset._showDetails = this.toggled === dataset.id
        return dataset
      })
    }
  },
  data() {
    return {
      dialog: false,
      treeViewOptions: {rootObjectKey: 'dataset', maxDepth: 0},
      toggled: undefined,
      fields: [
        { key: 'expected', 'class': 'f50' },
        { key: 'index', 'class': 'f50' },
        { label: 'Titre', align: 'left', key: 'title' },
      ],
    }
  },
  methods: {
    datasetUrl(id) {
      return `${this.details.server}/datasets/${id}/`
    },
    toggle(item, index) {
      this.toggled = this.toggled === item.id ? undefined : item.id
    },
  }
};
</script>

<style>
table.table caption {
  text-align: center;
  font-weight: bold;
  border: 1px solid lightgray;
  border-bottom: none;
}

.result-table thead {
  display: none;
}
</style>
