<template>
  <q-layout view="hhh lpR fFf">
    <TopHeader @hamburger-clicked="toggleLeftDrawer" />

    <LeftDrawer v-model="leftDrawerOpen" />

    <q-page-container>
      <router-view />
    </q-page-container>
  </q-layout>
</template>

<script lang="ts">
import { ref } from 'vue';

import TopHeader from 'components/identity/TopHeader.vue';
import LeftDrawer from 'components/identity/LeftDrawer.vue';

export default {
  name: 'MainLayout',
  components: {
    TopHeader,
    LeftDrawer,
  },
  setup() {
    const leftDrawerOpen = ref(false);

    return {
      leftDrawerOpen,
      toggleLeftDrawer() {
        leftDrawerOpen.value = !leftDrawerOpen.value;
      },
    };
  },
};
</script>
