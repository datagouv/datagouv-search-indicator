<template>
<div class="tree-view-wrapper">
  <tree-view-item class="tree-view-item-root"
    v-for="child in parsedData.children" :key="getKey(child)" :data="child"
    :current-depth="0" :max-depth="allOptions.maxDepth"
    :modifiable="allOptions.modifiable"  @change-data="onChangeData">
  </tree-view-item>
</div>
</template>

<script>
import Vue from 'vue'

export default {
  mixins: [Vue.options.components['tree-view']],
  methods: {
    getKey: function(value){
      if (Number.isInteger(value.key)) {
        return `${value.key}:`;
      } else {
        return `"${value.key}":`;
      }
    }
  }
}
</script>

<style>
.tree-view-wrapper {
  overflow: auto;
}
/* Find the first nested node and override the indentation */
.tree-view-item-root > .tree-view-item-leaf > .tree-view-item {
  margin-left: 0!important;
}
/* Root node should not be indented */
.tree-view-item-root {
  margin-left: 0!important;
}

.tree-view-item-hint {
  color: #82b1ff !important;
}
</style>
