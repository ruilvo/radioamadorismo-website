<template>
  <q-card bordered>
    <div class="row">
      <q-card-section class="col-xs-12 col-sm">
        <router-link
          class="text-h5"
          :to="{ name: 'blog-post-detail', params: { id: post.id } }"
          style="text-decoration: none; color: inherit"
        >
          {{ post.title }}
        </router-link>
        <div class="text-subtitle2">Criado em: {{ added }}</div>
      </q-card-section>
      <q-card-actions
        v-if="authStore.isAuthenticated"
        :vertical="$q.screen.gt.xs"
        class="col-auto"
      >
        <q-btn icon="edit" color="primary" @click="editAction">Editar</q-btn>
        <q-btn icon="delete" color="red" @click="deleteAction">Apagar</q-btn>
      </q-card-actions>
    </div>

    <q-separator inset />

    <q-card-section>
      <!-- eslint-disable-next-line vue/no-v-html -->
      <div v-html="post.intro"></div>
    </q-card-section>
  </q-card>
</template>

<script>
import { defineComponent, computed } from "vue";

import { useRouter } from "vue-router";

import useBlogStore from "src/stores/blog";
import useAuthStore from "src/stores/auth";

export default defineComponent({
  name: "BlogPostItem",
  props: {
    post: {
      type: Object,
      required: true,
    },
  },
  setup(props) {
    const $router = useRouter();

    const blogStore = useBlogStore();
    const authStore = useAuthStore();

    const added = computed(() => {
      return new Date(props.post.added).toLocaleString();
    });

    return {
      authStore,
      added,
      deleteAction() {
        const res = confirm("Tem a certeza que deseja apagar este post?");
        if (res)
          blogStore
            .deletePost(props.post.id)
            .then(() => $router.push({ name: "home" }));
      },
      editAction() {
        $router.push({ name: "blog-post-edit", params: { id: props.post.id } });
      },
    };
  },
});
</script>
