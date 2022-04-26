<template>
  <q-layout view="hhh lpr fff">
    <Header @hamburger-clicked="toggleLeftDrawer" />
    <Drawer v-model="leftDrawerOpen" />

    <q-page-container>
      <q-page padding :style-fn="pageStyleFn" class="scroll">
        <router-view />
      </q-page>
    </q-page-container>
  </q-layout>
</template>

<script>
import { defineComponent, ref } from "vue";

import { useQuasar } from "quasar";

import useAuthStore from "src/stores/auth";

import Header from "components/identity/Header.vue";
import Drawer from "components/identity/Drawer.vue";

export default defineComponent({
  // eslint-disable-next-line vue/multi-word-component-names
  name: "Main",
  components: {
    Header,
    Drawer,
  },
  setup() {
    const $q = useQuasar();

    const authStore = useAuthStore();
    authStore.check();

    const leftDrawerOpen = ref(false);

    return {
      leftDrawerOpen,
      toggleLeftDrawer() {
        leftDrawerOpen.value = !leftDrawerOpen.value;
      },
      pageStyleFn(offset, height) {
        return {
          [$q.screen.gt.xs ? "height" : "minHeight"]: `${height - offset}px`,
        };
      },
    };
  },
});
</script>
