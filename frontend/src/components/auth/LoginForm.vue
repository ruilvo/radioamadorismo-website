<template>
  <div class="q-pa-md" style="max-width: 400px">
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
  </div>
</template>

<script>
import { defineComponent, ref } from "vue";

import { useAuthStore } from "src/stores/auth";

export default defineComponent({
  setup() {
    const authStore = useAuthStore();

    const username = ref(null);
    const password = ref(null);
    const isPwd = ref(true);

    return {
      username,
      password,
      isPwd,

      onSubmit() {
        authStore.login({ username: username.value, password: password.value });
        // TODO: redirect or something, make it look something happened
      },
    };
  },
});
</script>
