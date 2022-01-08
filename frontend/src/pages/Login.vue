<template>
  <div class="flex flex-center full-height">
    <div class="column col-auto">
      <h4 class="text-center q-mb-md">Bem-vindo administrador(a)</h4>
      <q-banner v-if="hasError" class="text-white text-center bg-red q-mb-xl">
        <div>A autenticação falhou com erro:</div>
        <div>{{ errorMessage }}</div>
      </q-banner>
      <q-form class="q-gutter-sm" @submit="onSubmit">
        <q-input
          v-model="username"
          filled
          label="Nome de utilizador"
          lazy-rules
          :rules="[
            (val) =>
              (val && val.length > 0) ||
              'Por favor introduza um nome de utilizador',
          ]"
        />

        <q-input
          v-model="password"
          filled
          :type="isPwd ? 'password' : 'text'"
          hint="Password"
        >
          <template #append>
            <q-icon
              :name="isPwd ? 'visibility_off' : 'visibility'"
              class="cursor-pointer"
              @click="isPwd = !isPwd"
            />
          </template>
        </q-input>

        <div>
          <q-btn label="Entrar" type="submit" color="primary" />
        </div>
      </q-form>

      <q-linear-progress v-if="showProgress" query class="q-mt-md" />
    </div>
  </div>
</template>

<script>
import { defineComponent, ref, computed } from "vue";

import { useRouter } from "vue-router";

import useAuthStore from "src/stores/auth";

export default defineComponent({
  name: "Login",
  setup() {
    const $router = useRouter();

    const authStore = useAuthStore();
    authStore.$reset();

    const username = ref(null);
    const password = ref(null);
    const isPwd = ref(true);
    const showProgress = ref(false);

    const hasError = computed(() => {
      return authStore.errorMessage !== null;
    });

    const errorMessage = computed(() => {
      return authStore.errorMessage;
    });

    return {
      username,
      password,
      isPwd,
      hasError,
      errorMessage,
      showProgress,

      async onSubmit() {
        showProgress.value = true;
        await authStore.login(username.value, password.value);
        showProgress.value = false;
        if (!hasError.value) {
          $router.push({ name: "home" });
        }
      },
    };
  },
});
</script>
