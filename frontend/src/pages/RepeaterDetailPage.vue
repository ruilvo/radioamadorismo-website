<template>
  <div class="q-pa-md">
    <div class="q-gutter-md">
      <template v-if="repeater !== null">
        <h2>{{ props.id }}: {{ repeater?.callsign }}</h2>
        <q-separator />
        <FactRepeaterSection :repeater="repeater" />
        <InfoLocationSection
          v-if="repeater.info_location !== null"
          :info_location="repeater.info_location!"
        />
        <InfoHolderSection
          v-if="repeater.info_holder !== null"
          :info_holder="repeater.info_holder!"
        />
        <InfoRfSection
          v-if="repeater.info_rf !== null"
          :info_rf="repeater.info_rf!"
        />
        <InfoFmSection
          v-if="repeater.info_fm !== null"
          :info_fm="repeater.info_fm!"
        />
        <InfoDmrSection
          v-if="repeater.info_dmr !== null"
          :info_dmr="repeater.info_dmr!"
        />
        <InfoDstarSection
          v-if="repeater.info_dstar !== null"
          :info_dstar="repeater.info_dstar!"
        />
        <InfoFusionSection
          v-if="repeater.info_fusion !== null"
          :info_fusion="repeater.info_fusion!"
        />
        <InfoTetraSection
          v-if="repeater.info_tetra !== null"
          :info_tetra="repeater.info_tetra!"
        />
      </template>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, Ref } from 'vue';
import { api } from 'boot/axios';

import { paths, components } from 'src/types/api';

import InfoRfSection from 'components/repeaters/InfoRfSection.vue';
import InfoFmSection from 'components/repeaters/InfoFmSection.vue';
import InfoLocationSection from 'components/repeaters/InfoLocationSection.vue';
import InfoDstarSection from 'components/repeaters/InfoDstarSection.vue';
import InfoFusionSection from 'components/repeaters/InfoFusionSection.vue';
import InfoHolderSection from 'components/repeaters/InfoHolderSection.vue';
import InfoDmrSection from 'components/repeaters/InfoDmrSection.vue';
import InfoTetraSection from 'components/repeaters/InfoTetraSection.vue';
import FactRepeaterSection from 'components/repeaters/FactRepeaterSection.vue';

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
