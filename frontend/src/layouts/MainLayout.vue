<template>
  <q-layout view="hhh LpR fFf">
    <TopHeader @hamburger-clicked="left_drawer.toggle" />

    <LeftDrawer v-model="left_drawer.open" />

    <q-page-container>
      <router-view />
    </q-page-container>
  </q-layout>
</template>

<script setup lang="ts">
import TopHeader from 'components/identity/TopHeader.vue';
import LeftDrawer from 'components/identity/LeftDrawer.vue';

import { useLeftDrawerStore } from 'stores/left-drawer';

const left_drawer = useLeftDrawerStore();
</script>
