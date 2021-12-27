<template>
  <q-item key="about-url" clickable to="/sobre">
    <q-item-section avatar>
      <q-icon name="help_outline" />
    </q-item-section>
    <q-item-section>Sobre</q-item-section>
  </q-item>
</template>

<script>
import { defineComponent } from "vue";

export default defineComponent({
  name: "AboutItem",
});
</script>
