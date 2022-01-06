<template>
  <q-page padding>
    <h2>Perguntas de exame</h2>
    <hr />
  </q-page>
</template>

<script>
import { defineComponent } from "vue";

import BlogPosts from "components/BlogPosts.vue";

export default defineComponent({
  name: "Index",
  components: {
    BlogPosts,
  },
});
</script>
