<template>
  <div class="column q-gutter-md">
    <div class="col-auto">
      <q-btn
        v-if="authStore.isAuthenticated"
        icon="add"
        color="primary"
        @click="addAction"
        >Novo</q-btn
      >
    </div>

    <BlogPostItem
      v-for="post in blogStore.posts"
      :key="'post' + post.id"
      :post="post"
    />

    <div class="col-auto">
      <q-pagination
        v-model="currentPage"
        :max="numberPages"
        :max-pages="6"
        boundary-numbers
        class="row justify-center"
      />
    </div>
  </div>
</template>

<script>
import { defineComponent, ref, computed, watch } from "vue";

import { useRouter } from "vue-router";

import useBlogStore from "src/stores/blog";
import useAuthStore from "src/stores/auth";

import BlogPostItem from "./BlogPostItem.vue";

export default defineComponent({
  name: "BlogPosts",
  components: {
    BlogPostItem,
  },
  setup() {
    const $router = useRouter();

    const blogStore = useBlogStore();
    const authStore = useAuthStore();

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

    blogStore.updatePosts(offset.value, limit, false);

    return {
      blogStore,
      authStore,
      currentPage,
      numberPages,
      addAction() {
        $router.push({ name: "blog-post-new" });
      },
    };
  },
});
</script>
