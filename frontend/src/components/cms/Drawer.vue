<template>
  <q-drawer
    v-model="leftDrawerOpen"
    show-if-above
    side="left"
    bordered
    class="bg-grey-3"
  >
    <q-list>
      <q-item key="start" clickable to="/" exact>
        <q-item-section avatar>
          <q-icon name="home" />
        </q-item-section>
        <q-item-section>Página inicial</q-item-section>
      </q-item>
      <q-separator key="sep1" />
    </q-list>
  </q-drawer>
</template>

<script>
import { defineComponent, watch, ref, computed } from "vue";

import { useRoute } from "vue-router";

import useAuthStore from "src/stores/auth/auth";

export default defineComponent({
  name: "Drawer",
  props: {
    modelValue: Boolean,
  },
  emits: ["update:modelValue"],
  setup(props, { emit }) {
    const $route = useRoute();

    const authStore = useAuthStore();

    const repeaters_expanded = ref($route.path.includes("/repetidores"));
    const api_expanded = ref($route.path.includes("/swagger"));

    const isAuthenticated = computed(() => authStore.isAuthenticated);

    const leftDrawerOpen = computed({
      get: () => props.modelValue,
      set: (val) => {
        emit("update:modelValue", val);
      },
    });

    watch($route, (to) => {
      if (to.path.includes("/repetidores")) {
        repeaters_expanded.value = true;
      }
      if (to.path.includes("/swagger")) {
        api_expanded.value = true;
      }
    });

    return {
      leftDrawerOpen,
      repeaters_expanded,
      api_expanded,
      isAuthenticated,

      async logout() {
        await authStore.logout();
      },
    };
  },
});
</script>
