<template>
  <div class="q-pa-md">
    <div class="q-gutter-md">
      <h2>Gerador de Passcodes de APRS-IS</h2>
      <q-separator />
      <div class="row items-center q-gutter-x-md">
        <h4>Indicativo:</h4>
        <q-input v-model="callsign" filled dense square />
      </div>
      <q-btn
        color="primary"
        label="Submeter"
        class="col-auto"
        :disable="callsign === ''"
        @click="submit"
      />
      <h4 v-if="passcode != '' && !thinking" class="col-auto">
        O Passcode para o APRS-IS é: {{ passcode }}
      </h4>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { api } from 'boot/axios';

const callsign = ref('');
const passcode = ref('');
const thinking = ref(false);

const submit = () => {
  thinking.value = true;
  api
    .post('/api/v1/aprs/passcode-generator/', {
      callsign: callsign.value,
    })
    .then((response: { data: { passcode: string } }) => {
      passcode.value = response.data.passcode;
      thinking.value = false;
    });
};
</script>
