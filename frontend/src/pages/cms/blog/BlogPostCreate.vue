<template>
  <q-page class="row-auto justify-center">
    <h1 class="col-12 text-center">Criando um novo post</h1>
    <BlogCreateEditItem v-model="post" @submit="onSubmit" />
  </q-page>
</template>

<script>
import { defineComponent, ref } from "vue";

import { useRouter } from "vue-router";

import useCmsBlogStore from "src/stores/cms/blog";

import BlogCreateEditItem from "src/components/cms/blog/BlogCreateEditItem.vue";

export default defineComponent({
  name: "BlogPostCreate",
  components: {
    BlogCreateEditItem,
  },
  setup() {
    const $router = useRouter();

    const cmsBlogStore = useCmsBlogStore();

    const post = ref({
      title: "",
      intro: "",
      body: "",
    });

    return {
      post,

      onSubmit(newPost) {
        cmsBlogStore.createPost(newPost).then(() => {
          $router.push("/cms/blogue");
        });
      },
    };
  },
});
</script>
