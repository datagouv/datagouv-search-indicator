<template>
<b-row  v-if="item">
  <b-col cols="12" class="mb-3" :class="{'text-center': !model.oembed}">
    <o-embed v-if="model.oembed" :url="item.page"></o-embed>
    <a v-else :href="item.page">{{ item.title || item.name }}</a>
  </b-col>
  <b-col cols="12">
    <tree-view :data="item" :options="treeViewOptions"></tree-view>
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
import { mapActions, mapState } from "vuex"
import OEmbed from '../components/oembed.vue'
import TreeView from '../components/treeview.vue'

export default {
  name: 'item-details',
  props: {
    itemId: String,
  },
  components: {OEmbed, TreeView},
  computed: {
    ...mapState(['item', 'model'])
  },
  data() {
    return {
      treeViewOptions: {rootObjectKey: 'item', maxDepth: 0}
    }
  },
  created() {
    if (this.itemId) this.setItem(this.itemId)
  },
  methods: {
    ...mapActions(['setItem'])
  },
  watch: {
    itemId(id) {
      this.setItem(id)
    }
  }
}
</script>

<style>

</style>
