<template>
  <q-layout view="hhh lpr fff">
    <Header @hamburgerClicked="toggleLeftDrawer" />
    <Drawer v-model="leftDrawerOpen" />

    <q-page-container>
      <router-view />
    </q-page-container>
  </q-layout>
</template>

<script>
import { defineComponent, ref } from "vue";

import Header from "components/common/Header.vue";
import Drawer from "components/portal/Drawer.vue";

export default defineComponent({
  name: "MainLayout",
  components: {
    Header,
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
