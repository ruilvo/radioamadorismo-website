<template>
  <q-header bordered class="bg-primary text-white">
    <q-toolbar>
      <q-btn dense flat round icon="menu" @click="emitHamburgerClicked" />

      <q-toolbar-title class="row">
        <span class="text-italic q-mr-sm">Æ</span>
        <span class="q-mr-sm">Portal do Radioamadorismo</span>
        <span v-if="isOnCms" class="col text-center text-uppercase"
          >Painel de administração</span
        >
      </q-toolbar-title>
    </q-toolbar>
  </q-header>
</template>

<script>
import { defineComponent, computed } from "vue";

import { useRoute } from "vue-router";

import useAuthStore from "src/stores/auth/auth";

export default defineComponent({
  name: "Header",
  emits: {
    hamburgerClicked: null,
  },
  setup() {
    const $route = useRoute();

    const authStore = useAuthStore();
    authStore.check();

    const isOnCms = computed(() => $route.path.includes("/cms"));

    return {
      isOnCms,
      emitHamburgerClicked() {
        this.$emit("hamburgerClicked");
      },
    };
  },
});
</script>
