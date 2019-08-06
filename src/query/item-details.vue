<template>
<b-row  v-if="item"  align-h="center" >
  <b-col cols="12" :class="{
      'text-center': !model.oembed,
      'mb-3': !collapse,
      'mb-1': collapse,
    }" md="10" lg="8" >
    <o-embed v-if="model.oembed" :url="item.page"></o-embed>
    <b-button v-else variant="outline-primary" :href="item.page">
      {{ item.title || item.name }}
      <font-awesome-icon icon="external-link-alt"/>
    </b-button>
  </b-col>
  <b-col cols="12">
    <b-card v-if="collapse" no-body header-bg-variant="transparent">
      <b-card-header header-tag="header" class="p-0">
        <b-button block v-b-toggle.json-details variant="light">
          <font-awesome-icon icon="arrow-down"/>
          JSON
          <font-awesome-icon icon="arrow-down"/>
        </b-button>
      </b-card-header>
      <b-collapse id="json-details">
        <b-card-body body-bg-variant="light">
          <tree-view :data="item" :options="treeViewOptions"></tree-view>
        </b-card-body>
      </b-collapse>
    </b-card>
    <tree-view v-if="!collapse" :data="item" :options="treeViewOptions"></tree-view>
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
    item: Object,
    collapse: Boolean,
  },
  components: {OEmbed, TreeView},
  computed: {
    ...mapState(['model'])
  },
  data() {
    return {
      treeViewOptions: {rootObjectKey: 'item', maxDepth: 0}
    }
  },
}
</script>

<style>

</style>
