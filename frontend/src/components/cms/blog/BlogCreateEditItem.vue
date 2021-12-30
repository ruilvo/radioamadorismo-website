<template>
  <div class="q-pa-md">
    <q-form class="q-gutter-md" @submit="onSubmit">
      <q-input v-model="title" filled label="Título do post" />

      <q-input v-model="intro" filled type="textarea" label="Introdução" />

      <q-item-label>Corpo</q-item-label>
      <q-editor v-model="body" min-height="5rem" />

      <div>
        <q-btn label="Submeter" type="submit" color="primary" />
      </div>
    </q-form>
  </div>
</template>

<script>
import { defineComponent, ref, computed, watch } from "vue";

export default defineComponent({
  name: "BlogCreateEditItem",
  props: {
    modelValue: {
      type: Object,
      required: true,
    },
  },
  emits: ["update:modelValue", "submit"],
  setup(props, { emit }) {
    const editedPost = ref({ title: "", intro: "", body: "" });

    watch(props, (newVal) => {
      editedPost.value = newVal.modelValue;
    });

    const title = computed({
      get: () => editedPost.value.title,
      set: (val) => {
        editedPost.value.title = val;
        emit("update:modelValue", editedPost.value);
      },
    });

    const intro = computed({
      get: () => editedPost.value.intro,
      set: (val) => {
        editedPost.value.intro = val;
        emit("update:modelValue", editedPost.value);
      },
    });

    const body = computed({
      get: () => editedPost.value.body,
      set: (val) => {
        editedPost.value.body = val;
        emit("update:modelValue", editedPost.value);
      },
    });

    return {
      title,
      intro,
      body,
      onSubmit() {
        emit("submit", editedPost.value);
      },
    };
  },
});
</script>
