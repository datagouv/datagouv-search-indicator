<template>
<v-breadcrumbs>
  <v-icon slot="divider">forward</v-icon>
  <v-breadcrumbs-item v-for="route in $route.matched.filter(r => r.meta.breadcrumb)"
      :key="route.path" :to="route" exact>
    {{ label(route) }}
  </v-breadcrumbs-item>
</v-breadcrumbs>
</template>

<script>
export default {
  computed: {
    routes() {
      return this.$route.matched.filter(r => r.meta.breadcrumb)
    }
  },
  methods: {
    label(route) {
      if (route.meta.breadcrumb instanceof Function) {
        return route.meta.breadcrumb(this.$store)
      } else {
        return route.meta.breadcrumb
      }
    },
    to(route) {
      return {name: this.route.name, params: this.route.params}
    },
  }
}
</script>