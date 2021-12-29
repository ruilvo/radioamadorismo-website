<template>
  <q-page class="flex flex-center">
    <h1 class="text-center">BlogPostEdit</h1>
  </q-page>
</template>

<script>
import { defineComponent } from "vue";

export default defineComponent({
  name: "BlogPostEdit",
  props: {
    id: {
      type: String || Number,
      required: true,
    },
  },
});
</script>
