<template>
  <q-page padding>
    <q-btn @click="$router.push({ name: 'index' })"> Blog </q-btn>
  </q-page>
</template>

<script>
import { defineComponent } from "vue";

export default defineComponent({
  name: "BlogPostCreateEdit",
});
</script>
