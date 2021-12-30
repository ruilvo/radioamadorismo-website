<template>
  <router-link
    class="text-h6"
    :to="{ name: 'blog-detail', params: { id: post.id } }"
    style="text-decoration: none; color: inherit"
  >
    {{ post.title }}
  </router-link>

  <!-- eslint-disable-next-line vue/no-v-html -->
  <div v-html="post.intro"></div>

  <p>Criado em: {{ added }}</p>
</template>

<script>
import { defineComponent, computed } from "vue";

export default defineComponent({
  name: "BlogPostItem",
  props: {
    post: {
      type: Object,
      required: true,
    },
  },
  setup(props) {
    const added = computed(() => {
      return new Date(props.post.added).toLocaleString();
    });

    return {
      added,
    };
  },
});
</script>
