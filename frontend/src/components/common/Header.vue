<template>
  <q-header bordered class="bg-primary text-white">
    <q-toolbar>
      <q-btn
        v-if="!noHamburger"
        dense
        flat
        round
        icon="menu"
        @click="emitHamburgerClicked"
      />

      <q-toolbar-title class="row">
        <router-link to="/" style="text-decoration: none; color: inherit">
          <span class="text-italic q-mr-sm">Æ</span>
          <span class="q-mr-sm">Portal do Radioamadorismo</span>
        </router-link>

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
  props: {
    noHamburger: Boolean,
  },
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
