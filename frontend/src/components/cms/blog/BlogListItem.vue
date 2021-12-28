<template>
  <q-card class="row justify-between items-center q-ma-sm hover:tw-bg-gray-300">
    <q-card-section class="col">
      <div class="text-h5 q-mt-sm q-mb-xs">{{ post.id }}: {{ post.title }}</div>
      <div>Adicionado em {{ added }}</div>
    </q-card-section>

    <q-card-actions class="col-auto column">
      <q-btn flat><q-icon name="edit" />Editar</q-btn>
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

    return {
      added,
    };
  },
});
</script>
