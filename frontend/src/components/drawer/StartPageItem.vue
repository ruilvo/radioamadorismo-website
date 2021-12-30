<template>
  <q-item key="home-item" clickable to="/" exact>
    <q-item-section avatar>
      <q-icon name="home" />
    </q-item-section>
    <q-item-section>Página inicial</q-item-section>
  </q-item>
</template>

<script>
import { defineComponent } from "vue";

export default defineComponent({
  name: "StartPageItem",
});
</script>
