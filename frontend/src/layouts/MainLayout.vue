<template>
  <q-layout view="hhh LpR fFf">
    <TopHeader @hamburger-clicked="toggleLeftDrawer" />

    <LeftDrawer v-model="leftDrawerOpen" />

    <q-page-container>
      <router-view />
    </q-page-container>
  </q-layout>
</template>

<script setup lang="ts">
import { ref } from 'vue';

import TopHeader from 'components/identity/TopHeader.vue';
import LeftDrawer from 'components/identity/LeftDrawer.vue';

import { useLeftDrawerStore } from 'stores/left-drawer';

const left_drawer = useLeftDrawerStore();

const leftDrawerOpen = ref(true);

function toggleLeftDrawer() {
  // TODO(ruilvo, 2023-08-22): Remove useless variables.
  leftDrawerOpen.value = !leftDrawerOpen.value;
  left_drawer.open = leftDrawerOpen.value;
}
</script>
