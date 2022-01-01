<template>
  <q-page padding>
    <h2>Gerador de Passcodes de APRS-IS</h2>
    <div class="row">
      <h4 class="q-mr-md">Indicativo:</h4>
      <q-input v-model="callsign" filled />
    </div>
    <div class="row">
      <q-btn color="primary" label="Submeter" @click="submit" />
    </div>
    <div v-if="thinking" class="row">
      <q-circular-progress
        indeterminate
        size="50px"
        :thickness="0.22"
        color="lime"
        track-color="grey-3"
        class="q-ma-md"
      />
    </div>
    <div v-if="passcode != null && !thinking" class="row">
      <h4 class="q-mr-md">O Passcode para o APRS-IS é:</h4>
      <h4 class="tw-text-emerald-500">{{ passcode }}</h4>
    </div>
  </q-page>
</template>

<script>
import { defineComponent, ref } from "vue";

import { api } from "boot/axios";

export default defineComponent({
  name: "AprsPasscode",
  setup() {
    const callsign = ref("");
    const passcode = ref(null);
    const thinking = ref(false);
    return {
      callsign,
      passcode,
      thinking,
      submit() {
        thinking.value = true;
        api
          .post("/api/v1/aprs/passcode-generator/", {
            callsign: callsign.value,
          })
          .then((response) => {
            passcode.value = response.data.passcode;
            thinking.value = false;
          });
      },
    };
  },
});
</script>
