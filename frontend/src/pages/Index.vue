<template>
  <h2>Bem vindo(a) ao Portal do Radioamadorismo</h2>
  <hr />
  <BlogPostsList />
</template>

<script>
import { defineComponent } from "vue";

import BlogPostsList from "./BlogPostsList.vue";

export default defineComponent({
  name: "Index",
  components: {
    BlogPostsList,
  },
});
</script>
