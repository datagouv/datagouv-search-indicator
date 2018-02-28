<template>
<v-layout>
  <v-flex>
    <v-card class="ma-4">
      <v-card-text class="blue darken-1 white--text">
        <div class="display-2">Erreur {{ code }}</div>
      </v-card-text>
      <v-card-text>
        <p>{{ message }}</p>
      </v-card-text>
    </v-card>
  </v-flex>
</v-layout>
</template>

<script>
export default {
  data() {
    return {
      code: this.$route.query.code || 404,
      messages: {
          404: 'Page non trouvée.'
      },
      // message: this.$route.query.message || this.$t('Page Not Found.')
    }
  },
  computed: {
    message() {
      return this.$route.query.message || this.messages[this.code] || 'Une erreur inconnue est survenur'
    }
  }
}
</script>

<style>

</style>
