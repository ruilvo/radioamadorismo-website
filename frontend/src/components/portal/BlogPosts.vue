<template>
  <div class="q-gutter-sm">
    <BlogPostItem
      v-for="post in blogStore.posts"
      :key="'post' + post.id"
      :post="post"
    />
  </div>

  <q-pagination
    v-model="currentPage"
    :max="numberPages"
    :max-pages="6"
    boundary-numbers
    class="row justify-center"
  />
</template>

<script>
import { defineComponent, ref, computed, watch } from "vue";

import useBlogStore from "src/stores/blog";

import BlogPostItem from "./blog_posts/BlogPostItem.vue";

export default defineComponent({
  name: "BlogPosts",
  components: {
    BlogPostItem,
  },
  setup() {
    const blogStore = useBlogStore();

    const limit = 10;

    const currentPage = ref(1);
    const offset = computed(() => {
      return (currentPage.value - 1) * limit;
    });
    const numberPages = computed(() => {
      return Math.ceil(blogStore.count / limit);
    });
    watch(currentPage, () => {
      blogStore.updatePosts(offset.value, limit, false);
    });

    blogStore.updatePosts(offset, limit, false);

    return {
      blogStore,
      currentPage,
      numberPages,
    };
  },
});
</script>
