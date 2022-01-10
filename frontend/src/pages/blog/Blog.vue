<template>
  <h2 style="margin-bottom: 15px">Notícias e posts</h2>
  <div class="column q-col-gutter-md">
    <div class="col-auto">
      <q-btn
        v-if="isAuthenticated"
        icon="add"
        color="primary"
        @click="addAction"
        >Novo</q-btn
      >
    </div>

    <div v-for="post in posts" :key="'post' + post.id" class="col-auto">
      <PostListItem :post="post" />
    </div>

    <div class="col-auto">
      <div class="row justify-center">
        <q-pagination
          v-model="currentPage"
          :max="numberPages"
          :max-pages="6"
          :to-fn="toFn"
          boundary-numbers
          direction-links
          boundary-links
        />
      </div>
    </div>
  </div>
</template>

<script>
import { defineComponent, computed, ref, watch } from "vue";

import { useRouter } from "vue-router";

import useAuthStore from "src/stores/auth";
import useBlogStore from "src/stores/blog";

import PostListItem from "components/blog/PostListItem.vue";

export default defineComponent({
  name: "Blog",
  components: {
    PostListItem,
  },
  props: {
    page: {
      type: String,
      default: "1",
      requires: false,
    },
  },
  setup(props) {
    const $router = useRouter();

    const authStore = useAuthStore();
    const blogStore = useBlogStore();

    const limit = 10; // Posts per page

    const currentPage = ref(parseInt(props.page));
    watch(props, (newVal) => {
      currentPage.value = parseInt(newVal.page);
    });

    const isAuthenticated = computed(() => {
      return authStore.isAuthenticated;
    });
    const numberPages = computed(() => {
      return Math.ceil(blogStore.count / limit);
    });
    const posts = computed(() => {
      return blogStore.posts;
    });

    const updatePage = () => {
      const offset = (currentPage.value - 1) * limit;
      blogStore.updatePosts(offset, limit, false);
    };

    updatePage();
    watch(currentPage, updatePage);

    return {
      isAuthenticated,
      numberPages,
      currentPage,
      posts,
      addAction() {
        $router.push({ name: "blog-post-create" });
      },
      toFn(page) {
        return {
          name: "blog-posts-page",
          params: {
            page,
          },
        };
      },
    };
  },
});
</script>
