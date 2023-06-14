<template>
  <h2>Gerador de Passcodes de APRS-IS</h2>
  <div class="column q-col-gutter-md">
    <div class="col-auto">
      <div class="row q-col-gutter-sm">
        <h4 class="col-auto">Indicativo:</h4>
        <q-input v-model="callsign" class="col-auto" filled />
      </div>
    </div>

    <div class="col-auto">
      <q-btn color="primary" label="Submeter" @click="submit" />
    </div>
    <div v-if="passcode != null && !thinking" class="col-auto">
      <h4 class="q-mr-md">
        O Passcode para o APRS-IS é:
        <span class="tw-text-emerald-500">{{ passcode }}</span>
      </h4>
    </div>
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
