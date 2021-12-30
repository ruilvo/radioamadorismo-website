<template>
  <q-page class="row-auto justify-center">
    <h1 class="col-12 text-center">Editando o post: {{ id }}</h1>
    <BlogCreateEditItem v-model="post" @submit="onSubmit" />
  </q-page>
</template>

<script>
import { defineComponent, ref } from "vue";

import { useRouter } from "vue-router";

import useCmsBlogStore from "src/stores/cms/blog";

import BlogCreateEditItem from "src/components/cms/blog/BlogCreateEditItem.vue";

export default defineComponent({
  name: "BlogPostEdit",
  components: {
    BlogCreateEditItem,
  },
  props: {
    id: {
      type: String || Number,
      required: true,
    },
  },
  setup(props) {
    const $router = useRouter();

    const cmsBlogStore = useCmsBlogStore();

    const post = ref({});

    cmsBlogStore.getPost(props.id).then((res) => {
      post.value = res.data;
    });

    return {
      post,

      onSubmit(newPost) {
        cmsBlogStore.updatePost(props.id, newPost).then(() => {
          $router.push("/cms/blogue");
        });
      },
    };
  },
});
</script>
