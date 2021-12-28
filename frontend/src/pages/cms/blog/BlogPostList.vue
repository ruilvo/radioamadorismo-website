<template>
  <q-page class="row-auto">
    <h1 class="col-12 text-center">Lista de posts do blog</h1>
    <BlogListItem v-for="post in posts" :key="'post' + post.id" :post="post" />
  </q-page>
</template>

<script>
import { defineComponent, computed } from "vue";

import useCmsBlogStore from "src/stores/cms/blog";

import BlogListItem from "components/cms/blog/BlogListItem";

export default defineComponent({
  name: "BlogPostList",
  components: {
    BlogListItem,
  },
  setup() {
    const cmsBlogStore = useCmsBlogStore();

    cmsBlogStore.updatePosts();

    const posts = computed(() => {
      return cmsBlogStore.posts;
    });

    return {
      posts,
    };
  },
});
</script>
