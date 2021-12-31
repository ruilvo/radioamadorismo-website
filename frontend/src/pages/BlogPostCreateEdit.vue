<template>
  <q-page padding class="overflow-auto">
    <q-form class="q-gutter-md" @submit="onSubmit">
      <q-input v-model="title" filled label="Título" />

      <q-item-label>Introdução</q-item-label>
      <q-editor v-model="intro" min-height="5rem" />

      <q-item-label>Corpo</q-item-label>
      <q-editor v-model="body" min-height="5rem" />

      <div>
        <q-btn label="Enviar" type="submit" color="primary" />
      </div>
    </q-form>
  </q-page>
</template>

<script>
import { defineComponent, ref } from "vue";

import { useRouter } from "vue-router";

import useBlogStore from "src/stores/blog";

export default defineComponent({
  name: "BlogPostCreateEdit",
  props: {
    id: {
      type: String,
      required: false,
      default: null,
    },
  },
  setup(props) {
    const $router = useRouter();

    const blogStore = useBlogStore();

    const title = ref("");
    const intro = ref("");
    const body = ref("");

    // Default to create
    var onSubmit = (onSubmit = () => {
      blogStore
        .createPost({
          title: title.value,
          intro: intro.value,
          body: body.value,
        })
        .then(() => {
          $router.push({ name: "index" });
        });
    });

    if (props.id !== null) {
      // Means we are editing
      blogStore.getPost(props.id).then((response) => {
        title.value = response.data.title;
        intro.value = response.data.intro;
        body.value = response.data.body;
      });
      onSubmit = () => {
        blogStore
          .updatePost(props.id, {
            title: title.value,
            intro: intro.value,
            body: body.value,
          })
          .then(() => {
            $router.push({ name: "index" });
          });
      };
    }

    return {
      onSubmit,
      title,
      intro,
      body,
    };
  },
});
</script>
