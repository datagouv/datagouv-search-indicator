<template>
<v-layout v-if="dataset" column>
  <v-flex class="ma-3" xs12 md10 offset-md1 lg8 offset-lg2>
    <o-embed :url="dataset.page"></o-embed>
  </v-flex>
  <v-flex class="pa-1 blue lighten-5">
    <tree-view :data="dataset" :options="treeViewOptions"></tree-view>
  </v-flex>
</v-layout>
<v-layout v-else>
  <v-progress-circular indeterminate color="primary"></v-progress-circular>
</v-layout>
</template>

<script>
import { mapActions, mapGetters } from "vuex"
import OEmbed from '../components/oembed.vue'
import TreeView from '../components/treeview.vue'

export default {
  name: 'dataset-details',
  props: {
    datasetId: String,
  },
  components: {OEmbed, TreeView},
  computed: {
    ...mapGetters(['dataset'])
  },
  data() {
    return {
      treeViewOptions: {rootObjectKey: 'dataset', maxDepth: 0}
    }
  },
  created() {
    if (this.datasetId) this.setDataset(this.datasetId)
  },
  methods: {
    ...mapActions(['setDataset'])
  },
  watch: {
    datasetId(id) {
      this.setDataset(id)
    }
  }
}
</script>

<style>

</style>
