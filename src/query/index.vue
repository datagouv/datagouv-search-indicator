<template>
<div>
  <b-row>
    <b-col cols="12">
      <b-input-group>
        <b-input-group-prepend>
          <b-btn disabled variant="outline-primary">
            <font-awesome-icon icon="search" />
          </b-btn>
        </b-input-group-prepend>
        <b-form-input :value="query.query" />
      </b-input-group>
      <div class="param-list">
        <params-list :params="query.params"></params-list>
      </div>
      <div class="mb-3"></div>
    </b-col>
  </b-row>
  <b-row align-h="center" class="mb-3" v-if="query.error">
    <b-col cols="12">
      <b-alert variant="danger" show>
        <h4 class="alert-heading">Erreur durant le traitement de la requête</h4>
        {{ query.error }}
      </b-alert>
    </b-col>
  </b-row>
  <item-details :item="expected" collapse></item-details>
  <div class="mb-3"></div>
  <b-table striped outlined hover caption-top fixed show-empty class="result-table"
      :items="items" :fields="fields" @row-clicked="toggle"
      empty-text="Aucun résultat"
      tbody-tr-class="clickable">
    <template slot="table-caption" v-if="query.found">
      {{ model.singular }} trouvé<span v-if="model.feminine">e</span> parmi {{ query.total }} resultats
    </template>
    <template slot="table-caption" v-if="!query.found && query.total">
      {{ model.singular }} non trouvé<span v-if="model.feminine">e</span> parmi {{ query.total }} resultats
    </template>
    <template slot="expected" slot-scope="data">
      <font-awesome-icon v-if="data.item.id === query.expected"
        icon="star" style="color: yellow"/>
    </template>
    <template slot="index" slot-scope="data">
      {{ data.index + 1 }}
    </template>
    <template slot="row-details" slot-scope="row">
      <item-details :item="item"></item-details>
    </template>
  </b-table>
</div>
</template>

<script>
import { mapActions, mapState } from "vuex"
import OEmbed from '../components/oembed.vue'
import ItemDetails from './item-details.vue'
import ParamsList from './param-list.vue'

export default {
  components: {OEmbed, ItemDetails, ParamsList},
  computed: {
    ...mapState(['query', 'details', 'model', 'expected', 'item']),
    items() {
      return this.query.items.map(item => {
        item._showDetails = this.toggled === item.id
        return item
      })
    },
  },
  data() {
    return {
      dialog: false,
      treeViewOptions: {rootObjectKey: 'item', maxDepth: 0},
      toggled: undefined,
      fields: [
        { key: 'expected', 'class': 'f50' },
        { key: 'index', 'class': 'f50' },
        { label: 'Titre', align: 'left', key: 'title' },
      ],
    }
  },
  methods: {
    urlFor(id) {
      return `${this.details.server}/${this.model.path}/${id}/`
    },
    toggle(item, index) {
      this.toggled = this.toggled === item.id ? undefined : item.id
    },
    ...mapActions(['setItem'])
  },
  watch: {
    toggled(itemId) {
      this.setItem(itemId)
    }
  }
};
</script>

<style scoped>
table.table >>> caption {
  text-align: center;
  font-weight: bold;
  border: 1px solid lightgray;
  border-bottom: none;
}

.result-table >>> thead {
  display: none;
}

>>> .param-list {
  padding-left: 45px;
}
</style>
