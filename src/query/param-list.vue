<template>
<div v-show="allParams.length">
  <b-badge v-for="param in allParams" variant="primary" :key="param.key" :title="param.label">
    <font-awesome-icon :icon="{prefix: param.iconPrefix || 'fas', iconName: param.icon}" />
    {{ param.value }}
  </b-badge>
</div>
</template>

<script>
import facets from '../facets'

export default {
  name: 'params-list',
  props: {
    params: Object,
  },
  computed: {
    allParams() {
      const params = []
      for (const [key, value] of Object.entries(this.params)) {
        if (Array.isArray(value)) {
          value.forEach(entry => {
            params.push({
              key,
              value: entry,
            })
          })
        } else {
          params.push({
            key, value
          })
        }
      }
      return params.map(param => Object.assign(param, facets[param.key]))
    }
  },
};
</script>

<style>
</style>
