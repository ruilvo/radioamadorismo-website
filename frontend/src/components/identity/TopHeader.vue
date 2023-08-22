<template>
  <q-header bordered class="bg-primary text-white">
    <q-toolbar>
      <q-btn
        flat
        dense
        round
        icon="menu"
        aria-label="Menu"
        @click="emitHamburgerClicked"
      />

      <q-toolbar-title class="row">
        <router-link to="/" style="text-decoration: none; color: inherit">
          <span class="text-italic q-mr-sm">Æ</span>
          <span class="q-mr-sm">Portal do Radioamador</span>
        </router-link>
      </q-toolbar-title>
    </q-toolbar>
  </q-header>
</template>

<script setup lang="ts">
const emit = defineEmits(['hamburgerClicked']);

function emitHamburgerClicked() {
  emit('hamburgerClicked');
}
</script>
