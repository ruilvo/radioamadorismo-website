<template>
  <q-page padding>
    <h2>Bem vindo(a) ao Portal do Radioamadorismo</h2>
    <hr />
    <h2 style="margin-bottom: 15px">Notícias e posts</h2>
    <BlogPosts />
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
