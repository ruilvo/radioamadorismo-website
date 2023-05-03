<template>
  <q-item key="home-item" clickable :to="{ name: 'home' }" exact>
    <q-item-section avatar>
      <q-icon name="home" />
    </q-item-section>
    <q-item-section>Página inicial</q-item-section>
  </q-item>
</template>

<script lang="ts">
import { defineComponent } from 'vue';

export default defineComponent({
  name: 'StartPageItem',
});
</script>
