<template>
  <div class="oembed">
    <div class="oembed-box oembed-loading" v-if="!oembed.type && !error">
      <font-awesome-icon icon="spinner" pulse/>
    </div>
    <div class="oembed-box oembed-error" v-if="error">
      {{ error }}
    </div>
    <div class="oembed-content" v-if="oembed.type" v-html="oembed.html"></div>
  </div>
</template>

<script>
import {mapGetters} from 'vuex'

export default {
  name: 'o-embed',
  props: {
    url: {
      type: String,
      required: true
    }
  },
  data () {
    return {
      oembed: Object,
      error: undefined,
    }
  },
  computed: {
    ...mapGetters(['oembedApi'])
  },
  async created() {
    this.getOembed(this.url)
  },
  methods: {
    async getOembed(url) {
      this.error = undefined
      this.oembed = {}
      if (!url) return;
      try {
        const oembedUrl = `${this.oembedApi}?url=${encodeURIComponent(url)}`
        const response = await fetch(oembedUrl)
        if (response.ok) {
          this.oembed = await response.json()
        } else {
          this.error = response.statusText
        }
      } catch(error) {
        this.error = error
      }
    }
  },
  watch: {
    url(value) {
      this.getOembed(value)
    }
  }
}
</script>

<style scoped>
.oembed-box {
  padding: 15px;
  border: 1px solid lightgrey;
  border-radius: 0.2em;
  text-align: center;
}

.oembed-error {
  border: 2px solid red;
  background-color: #f5c6cb;
}
</style>
