<template>
  <h2>Bem vindo(a) ao Portal do Radioamadorismo</h2>
  <hr />
  <h2 style="margin-bottom: 15px">Notícias e posts</h2>
  <!-- <BlogPosts /> -->
</template>

<script>
import { defineComponent } from "vue";

import BlogPosts from "components/BlogPosts.vue";

export default defineComponent({
  name: "Index",
  components: {
    // BlogPosts,
  },
});
</script>
