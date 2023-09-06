<template>
  <div class="q-pa-md">
    <div v-if="repeater === null">
      <q-spinner-gears />
    </div>
    <div v-else>
      <div class="q-gutter-md">
        <h2>{{ props.id }}: {{ repeater?.callsign }}</h2>
        <q-separator />
        <InfoRfSection
          v-if="repeater.info_rf !== null"
          :info_rf="repeater.info_rf!"
        />
        <InfoFmSection
          v-if="repeater.info_fm !== null"
          :info_fm="repeater.info_fm!"
        />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, Ref } from 'vue';
import { api } from 'boot/axios';

import { paths, components } from 'src/types/api';

import InfoRfSection from 'components/repeaters/InfoRfSection.vue';
import InfoFmSection from 'components/repeaters/InfoFmSection.vue';

type FactRepeater = components['schemas']['FactRepeater'];
type FactRepeaterIdResponse =
  paths['/api/v1/repeaters/fact-repeater/{id}/']['get']['responses']['200']['content']['application/json'];

const props = defineProps({
  id: String,
});

const repeater: Ref<FactRepeater | null> = ref(null);

onMounted(() => {
  api
    .get<FactRepeaterIdResponse>('/api/v1/repeaters/fact-repeater/' + props.id)
    .then((response) => {
      repeater.value = response.data;
    })
    .catch((error) => {
      console.error(error);
    });
});
</script>
