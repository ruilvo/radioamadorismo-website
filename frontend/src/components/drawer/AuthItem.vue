<template>
  <q-item
    v-if="!isAuthenticated"
    key="login-entry"
    clickable
    :to="{ name: 'login' }"
  >
    <q-item-section avatar>
      <q-icon name="login" />
    </q-item-section>
    <q-item-section>Entrar</q-item-section>
  </q-item>
  <q-item
    v-if="isAuthenticated"
    key="django-admin-entry"
    tag="a"
    href="/admin"
    clickable
  >
    <q-item-section avatar>
      <q-icon name="settings" />
    </q-item-section>
    <q-item-section>Django-admin</q-item-section>
  </q-item>
  <q-item v-if="isAuthenticated" key="logout-entry" clickable @click="logout">
    <q-item-section avatar>
      <q-icon name="logout" />
    </q-item-section>
    <q-item-section>Sair</q-item-section>
  </q-item>
</template>

<script>
import { defineComponent, computed } from "vue";

import { useRouter } from "vue-router";

import useAuthStore from "src/stores/auth";

export default defineComponent({
  name: "AuthItem",
  setup() {
    const $router = useRouter();

    const authStore = useAuthStore();

    const isAuthenticated = computed(() => authStore.isAuthenticated);

    return {
      isAuthenticated,

      async logout() {
        await authStore.logout();
        $router.push({ name: "home" });
      },
    };
  },
});
</script>
