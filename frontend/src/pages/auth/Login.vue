<template>
  <q-page class="flex flex-center">
    <div class="q-pa-md col" style="max-width: 400px">
      <q-banner v-if="hasError" class="text-white text-center bg-red q-mb-xl">
        <div>A autenticação falhou com erro:</div>
        <div>{{ errorMessage }}</div>
      </q-banner>
      <q-form class="q-gutter-md" @submit="onSubmit">
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
  </q-page>
</template>

<script>
import { defineComponent, ref, computed } from "vue";

import { useRouter } from "vue-router";

import useAuthStore from "src/stores/auth/auth";

export default defineComponent({
  name: "LoginPage",
  setup() {
    const router = useRouter();

    const authStore = useAuthStore();
    authStore.errorMessage = null; // Start with an empty error message

    const username = ref(null);
    const password = ref(null);
    const isPwd = ref(true);
    const showProgress = ref(false);

    const hasError = computed(() => {
      return !!authStore.errorMessage;
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

      onSubmit() {
        showProgress.value = true;
        authStore.login({ username: username.value, password: password.value });
        showProgress.value = false;
        if (!hasError.value) {
          router.push("/");
        }
      },
    };
  },
});
</script>
