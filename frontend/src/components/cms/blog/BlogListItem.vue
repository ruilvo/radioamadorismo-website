<template>
  <q-card class="row justify-between items-center q-ma-sm hover:tw-bg-gray-300">
    <router-link v-slot="{ href, navigate }" :to="editUrl" custom>
      <q-card-section
        tag="a"
        class="col"
        :href="href"
        style="cursor: pointer"
        @click="navigate"
      >
        <div class="text-h5 q-mt-sm q-mb-xs">
          {{ post.id }}: {{ post.title }}
        </div>
        <div>Adicionado em {{ added }}</div>
      </q-card-section>
    </router-link>

    <q-card-actions class="col-auto column">
      <q-btn flat
        ><q-icon name="edit" /><router-link :to="editUrl"
          >Editar</router-link
        ></q-btn
      >
      <q-btn flat><q-icon name="delete" />Apagar</q-btn>
    </q-card-actions>
  </q-card>
</template>

<script>
import { defineComponent, computed } from "vue";

export default defineComponent({
  name: "BlogListItem",
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

    const editUrl = computed(() => {
      return { name: "blog-post-edit", params: { id: props.post.id } };
    });

    return {
      added,
      editUrl,
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
