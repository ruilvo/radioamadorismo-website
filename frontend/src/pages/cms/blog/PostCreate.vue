<template>
  <q-page class="row-auto justify-center q-mx-sm">
    <h1 class="col-12 text-center">Criando um novo post</h1>
    <Editor v-model="post" @submit="onSubmit" />
  </q-page>
</template>

<script>
import { defineComponent, ref } from "vue";

import { useRouter } from "vue-router";

import useCmsBlogStore from "src/stores/blog";

import Editor from "components/cms/blog/Editor.vue";

export default defineComponent({
  name: "PostCreate",
  components: {
    Editor,
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
