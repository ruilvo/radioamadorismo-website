<template>
  <q-card class="row justify-between items-center hover:tw-bg-gray-300">
    <router-link v-slot="{ href, navigate }" :to="editUrl" custom>
      <q-card-section
        tag="a"
        class="col"
        :href="href"
        style="cursor: pointer"
        @click="navigate"
      >
        <div class="text-h5 q-mb-xs">
          {{ post.title }}
        </div>
        <div>Adicionado em {{ added }}</div>
      </q-card-section>
    </router-link>

    <q-card-actions class="col-auto" vertical>
      <q-btn color="secondary"
        ><q-icon name="edit" /><router-link :to="editUrl"
          >Editar</router-link
        ></q-btn
      >
      <q-btn color="red" @click="deletePost"
        ><q-icon name="delete" />Apagar</q-btn
      >
    </q-card-actions>
  </q-card>
</template>

<script>
import { defineComponent, computed } from "vue";

import useCmsBlogStore from "src/stores/cms/blog";

export default defineComponent({
  name: "ListItem",
  props: {
    post: {
      type: Object,
      required: true,
    },
  },
  setup(props) {
    const cmsBlogStore = useCmsBlogStore();

    const added = computed(() => {
      return new Date(props.post.added).toLocaleString();
    });

    const editUrl = computed(() => {
      return { name: "cms-blog-post-edit", params: { id: props.post.id } };
    });

    return {
      added,
      editUrl,
      deletePost() {
        if (confirm("Tem a certeza que quer apagar o post?")) {
          cmsBlogStore.deletePost(props.post.id).then(cmsBlogStore.updatePosts);
        }
      },
    };
  },
});
</script>

<style>
a:link {
  text-decoration: inherit;
  color: inherit;
  cursor: auto;
}

a:visited {
  text-decoration: inherit;
  color: inherit;
  cursor: auto;
}
</style>
