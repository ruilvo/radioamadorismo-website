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

      <div v-if="authStore.isAuthenticated" class="overflow-auto q-mt-md">
        <div class="q-gutter-md">
          <q-btn icon="edit" color="primary" @click="editAction">Editar</q-btn>
          <q-btn icon="delete" color="red" @click="deleteAction">Apagar</q-btn>
        </div>
      </div>
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

import { useRouter } from "vue-router";

import useBlogStore from "src/stores/blog";
import useAuthStore from "src/stores/auth";

export default defineComponent({
  name: "BlogPostDetail",
  props: {
    id: {
      type: String,
      required: true,
    },
  },
  setup(props) {
    const $router = useRouter();

    const blogStore = useBlogStore();
    const authStore = useAuthStore();

    const post = ref(null);

    blogStore.getPost(props.id).then((response) => {
      post.value = response.data;
    });

    const added = computed(() => {
      return new Date(post.value.added).toLocaleString();
    });

    return {
      authStore,
      post,
      added,
      deleteAction() {
        const res = confirm("Are you sure you want to delete this post?");
        if (res)
          blogStore
            .delete(props.id)
            .then(() =>
              $router.push({ name: "index", params: { id: props.id } })
            );
      },
      editAction() {
        $router.push({ name: "blog-edit", params: { id: props.id } });
      },
    };
  },
});
</script>
