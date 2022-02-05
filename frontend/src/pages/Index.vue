<template>
  <h2>Bem-vindo(a) ao Portal do Radioamadorismo</h2>
  <hr />
  <Blog />
</template>

<script>
import { defineComponent } from "vue";

import Blog from "./blog/Blog.vue";

export default defineComponent({
  name: "Index",
  components: {
    Blog,
  },
});
</script>
