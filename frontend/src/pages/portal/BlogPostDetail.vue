<template>
  <q-page padding>
    <div v-if="!!post">
      <div class="text-h4">{{ post.title }}</div>
      <div class="text-subtitle2">Criado em: {{ added }}</div>

      <div class="q-my-lg">
        <!-- eslint-disable-next-line vue/no-v-html -->
        <div v-html="post.intro"></div>
      </div>

      <!-- eslint-disable-next-line vue/no-v-html -->
      <div v-html="post.body"></div>
    </div>
    <div v-if="!post" class="row justify-center">
      <q-circular-progress
        indeterminate
        size="50px"
        :thickness="0.22"
        color="lime"
        track-color="grey-3"
        class="q-ma-md"
      />
    </div>
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

    const post = ref(null);

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
