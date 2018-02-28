<template>
<v-card>
  <v-container fluid>
    <v-layout row wrap>
      <v-flex xs-12 sm-10>

      <v-text-field prepend-icon="search" :value="query.query" hide-details single-line></v-text-field>
      </v-flex>
      <v-flex xs-6 sm-1>
        <v-checkbox :label="`Found: ${query.found}`" v-model="query.found"></v-checkbox>
      </v-flex>
      <v-flex xs-6 sm-1>Total: {{ query.total }}</v-flex>
    </v-layout>
    <v-layout row>
      <v-flex xs6>
        <v-list>
          <v-list-tile v-for="(dataset, index) in query.datasets" :key="dataset.id"
            @click="setDataset(dataset.id)">
            <v-list-tile-content>
              <v-list-tile-title>{{ index }}. {{ dataset.title }}</v-list-tile-title>
            </v-list-tile-content>
          </v-list-tile>
        </v-list>
      </v-flex>
      <v-flex xs6 v-if="dataset">
        <v-layout column>
          <v-flex>
            <p class="text-xs-center">
              Dataset {{ dataset.id }}
              <v-btn flat icon color="indigo" target="_blank" :href="dataset.page">
                <v-icon>open_in_new</v-icon>
              </v-btn>
            </p>
          </v-flex>
          <v-flex>
            <tree-view :data="dataset" :options="treeViewOptions"></tree-view>
          </v-flex>
        </v-layout>
      </v-flex>
      <v-flex xs6 v-else>
        <p class="text-xs-center">Pick a dataset</p>
      </v-flex>
    </v-layout>
  </v-container>
</v-card>
</template>

<script>
import { mapActions, mapGetters } from "vuex"

export default {
  computed: {
    ...mapGetters(['query', 'dataset'])
  },
  data() {
    return {
      treeViewOptions: {rootObjectKey: 'dataset', maxDepth: 1}
    }
  },
  methods: {
    ...mapActions(['setDataset']),
  }
};
</script>

<style>

</style>
