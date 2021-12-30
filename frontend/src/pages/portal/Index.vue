<template>
  <q-page padding>
    <h2>Bem vindo(a) ao Portal do Radioamadorismo</h2>
    <p>
      Lorem ipsum dolor sit amet consectetur adipisicing elit. Fugit nihil
      praesentium molestias a adipisci, dolore vitae odit, quidem consequatur
      optio voluptates asperiores pariatur eos numquam rerum delectus commodi
      perferendis voluptate?
    </p>
    <hr />
    <h2 class="q-mb-md">Notícias e posts</h2>
    <BlogPosts />
  </q-page>
</template>

<script>
import { defineComponent } from "vue";

import BlogPosts from "components/portal/BlogPosts.vue";

export default defineComponent({
  name: "Index",
  components: {
    BlogPosts,
  },
});
</script>
