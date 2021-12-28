<template>
  <q-item key="blog-url" clickable to="/cms/blogue">
    <q-item-section avatar>
      <q-icon name="article" />
    </q-item-section>
    <q-item-section>Blogue</q-item-section>
  </q-item>
</template>

<script>
import { defineComponent } from "vue";

export default defineComponent({
  name: "BlogItem",
});
</script>
