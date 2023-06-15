<template>
  <div class="q-pa-md q-gutter-y-md">
    <h2>Gerador de Passcodes de APRS-IS</h2>
    <div class="row items-center q-gutter-x-md">
      <h4 class="col-auto">Indicativo:</h4>
      <q-input v-model="callsign" class="col-auto" filled />
    </div>
    <div class="row items-center">
      <q-btn
        color="primary"
        label="Submeter"
        class="col-auto"
        :disable="callsign === ''"
        @click="submit"
      />
    </div>
    <h4 v-if="passcode != null && !thinking" class="col-auto">
      O Passcode para o APRS-IS é: {{ passcode }}
    </h4>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue';

import { api } from 'boot/axios';

export default defineComponent({
  name: 'AprsPasscodePage',
  setup() {
    const callsign = ref('');
    const passcode = ref(null);
    const thinking = ref(false);

    return {
      callsign,
      passcode,
      thinking,
      submit() {
        thinking.value = true;
        api
          .post('/api/v1/aprs/passcode-generator/', {
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
