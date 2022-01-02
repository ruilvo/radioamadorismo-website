<template>
  <q-page padding class="overflow-auto">
    <q-banner v-if="hasError" class="text-white text-center bg-red q-mb-xl">
      <div>Todos os campos são obrigatórios!</div>
    </q-banner>
    <q-form class="q-gutter-md" @submit="onSubmit">
      <q-input v-model="title" filled label="Título" />

      <q-item-label>Introdução</q-item-label>
      <RichTextEditor v-model="intro" />

      <q-item-label>Corpo</q-item-label>
      <RichTextEditor v-model="body" />

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

import RichTextEditor from "components/RichTextEditor";

export default defineComponent({
  name: "BlogPostCreateEdit",
  components: {
    RichTextEditor,
  },
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

    const hasError = ref(false);

    const title = ref("");
    const intro = ref("");
    const body = ref("");

    const validateForm = () => {
      hasError.value = false;

      if (!title.value || title.value === "") {
        hasError.value = true;
      }

      if (!intro.value || intro.value === "") {
        hasError.value = true;
      }

      if (!body.value || body.value === "") {
        hasError.value = true;
      }
    };

    // Default to create
    var onSubmit = () => {
      validateForm();
      if (hasError.value) return;
      blogStore
        .createPost({
          title: title.value,
          intro: intro.value,
          body: body.value,
        })
        .then(() => {
          $router.push({ name: "index" });
        });
    };

    if (props.id !== null) {
      // Means we are editing
      blogStore.getPost(props.id).then((response) => {
        title.value = response.data.title;
        intro.value = response.data.intro;
        body.value = response.data.body;
      });
      onSubmit = () => {
        validateForm();
        if (hasError.value) return;
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
      hasError,
      onSubmit,
      title,
      intro,
      body,
    };
  },
});
</script>
