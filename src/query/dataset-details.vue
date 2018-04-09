<template>
<b-row  v-if="dataset">
  <b-col cols="12" class="mb-3">
    <o-embed :url="dataset.page"></o-embed>
  </b-col>
  <b-col cols="12">
    <tree-view :data="dataset" :options="treeViewOptions"></tree-view>
  </b-col>
</b-row>
<b-row v-else>
  <b-col cols="12">
    <p class="text-center">
      <font-awesome-icon icon="spinner" pulse/>
    </p>
  </b-col>
</b-row>
</template>

<script>
import { mapActions, mapGetters } from "vuex"
import OEmbed from '../components/oembed.vue'
import TreeView from '../components/treeview.vue'
import FontAwesomeIcon from '@fortawesome/vue-fontawesome'

export default {
  name: 'dataset-details',
  props: {
    datasetId: String,
  },
  components: {FontAwesomeIcon, OEmbed, TreeView},
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
