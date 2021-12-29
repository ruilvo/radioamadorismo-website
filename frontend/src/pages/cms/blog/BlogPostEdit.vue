<template>
  <q-page class="row-auto justify-center">
    <h1 class="col-12 text-center">Editando o post: {{ id }}</h1>
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
  </q-page>
</template>

<script>
import { defineComponent, ref } from "vue";

import { useRouter } from "vue-router";

import { api } from "boot/axios";

export default defineComponent({
  name: "BlogPostEdit",
  props: {
    id: {
      type: String || Number,
      required: true,
    },
  },
  setup(props) {
    const $router = useRouter();

    const post = ref({});

    const title = ref("");
    const intro = ref("");
    const body = ref("");

    api.get(`/api/v1/cms/fact-blog-post/${props.id}`).then((res) => {
      post.value = res.data;
      title.value = res.data.title;
      intro.value = res.data.intro;
      body.value = res.data.body;
    });

    return {
      post,
      title,
      intro,
      body,

      onSubmit() {
        post.value.title = title.value;
        post.value.intro = intro.value;
        post.value.body = body.value;
        api
          .put(`/api/v1/cms/fact-blog-post/${props.id}/`, post.value)
          .then(() => {
            $router.push("/cms/blogue/");
          })
          .catch((err) => {
            console.log(err);
          });
      },
    };
  },
});
</script>
