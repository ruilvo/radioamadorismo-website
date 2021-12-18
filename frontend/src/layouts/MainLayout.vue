<template>
  <q-layout view="hhh lpr fff">
    <q-header bordered class="bg-primary text-white">
      <q-toolbar>
        <q-btn dense flat round icon="menu" @click="toggleLeftDrawer" />

        <q-toolbar-title>
          <span class="text-italic q-mr-sm">Æ</span>
          <span class="q-mr-sm">Portal do Radioamadorismo</span>
          <span class="text-caption">Um projeto de Rui "CT7ALW" Oliveira</span>
        </q-toolbar-title>
      </q-toolbar>
    </q-header>

    <Drawer v-model="leftDrawerOpen" />

    <q-page-container>
      <router-view />
    </q-page-container>
  </q-layout>
</template>

<script>
import { defineComponent, ref } from "vue";

import Drawer from "src/components/drawer/Drawer.vue";

export default defineComponent({
  name: "MainLayout",
  components: {
    Drawer,
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
});
</script>
