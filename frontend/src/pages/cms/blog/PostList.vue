<template>
  <q-page class="row-auto q-mx-sm">
    <h1 class="col-12 text-center">Lista de posts do blog</h1>
    <div class="q-gutter-sm">
      <q-btn class="q-my-sm" color="primary" @click="createPost"
        ><q-icon name="add" />Criar</q-btn
      >
      <ListItem v-for="post in posts" :key="'post' + post.id" :post="post" />
    </div>
  </q-page>
</template>

<script>
import { defineComponent, computed } from "vue";

import { useRouter } from "vue-router";

import useCmsBlogStore from "src/stores/cms/blog";

import ListItem from "components/cms/blog/ListItem";

export default defineComponent({
  name: "PostList",
  components: {
    ListItem,
  },
  setup() {
    const $router = useRouter();

    const cmsBlogStore = useCmsBlogStore();

    cmsBlogStore.updatePosts();

    const posts = computed(() => {
      return cmsBlogStore.posts;
    });

    return {
      posts,
      createPost() {
        $router.push("/cms/blogue/novo");
      },
    };
  },
});
</script>
