<template>
<b-breadcrumb :items="items" />
</template>

<script>
export default {
  computed: {
    items() {
      const length = this.routes.length
      return this.routes.map((route, i) => this.item(route, i + 1 == length))
    },
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
      return {name: route.name || route.meta.default, params: route.params}
    },
    item(route, active) {
      return {text: this.label(route), to: this.to(route), active}
    }
  }
}
</script>
