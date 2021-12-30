<template>
  <q-page padding>
    <div class="text-h6">{{ post.title }}</div>
    <!-- eslint-disable-next-line vue/no-v-html -->
    <div v-html="post.intro"></div>

    <!-- eslint-disable-next-line vue/no-v-html -->
    <div v-html="post.body"></div>

    <p>Criado em: {{ added }}</p>
  </q-page>
</template>

<script>
import { defineComponent, computed, ref } from "vue";

import useBlogStore from "src/stores/blog";

export default defineComponent({
  name: "BlogPostDetail",
  props: {
    id: {
      type: String,
      required: true,
    },
  },
  setup(props) {
    const blogStore = useBlogStore();

    const post = ref({});

    blogStore.getPost(props.id).then((response) => {
      post.value = response.data;
    });

    const added = computed(() => {
      return new Date(post.value.added).toLocaleString();
    });

    return {
      post,
      added,
    };
  },
});
</script>
