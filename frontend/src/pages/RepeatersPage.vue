<template>
  <div class="q-pa-md">
    <div class="q-gutter-md">
      <h2>Repetidores</h2>
      <q-separator />
      <q-banner inline-actions class="text-white bg-red">
        <h5><b>Página em construção.</b></h5>
        Mais detalhes podem ser consultados usando diretamente a API, usando as
        ligações na barra lateral.
      </q-banner>
      <q-card flat>
        <q-tabs v-model="tab">
          <q-tab name="list" label="Listagem" />
          <q-tab name="map" label="Mapa" />
          <q-tab name="export" label="Exportar (Codeplugs)" />
        </q-tabs>
        <q-separator />
        <q-tab-panels v-model="tab" animated>
          <q-tab-panel name="list">
            <div class="q-gutter-y-md">
              <h3>Listagem de repetidores</h3>
              <RepeatersTable :repeaters="repeaters" />
            </div>
          </q-tab-panel>
          <q-tab-panel name="map">
            <div class="q-gutter-y-md">
              <h3>Mapa de repetidores</h3>
              <RepeatersMap :repeaters="repeaters" />
            </div>
          </q-tab-panel>
          <q-tab-panel name="export">
            <div class="q-gutter-y-md">
              <h3>Exportação</h3>
              <RepeatersExport />
            </div>
          </q-tab-panel>
        </q-tab-panels>
      </q-card>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, Ref, watch } from 'vue';

import { useQuasar } from 'quasar';

import { api } from 'boot/axios';

import { AxiosResponse } from 'axios';

import { paths, components } from 'src/types/api';

import RepeatersTable from 'components/repeaters/RepeatersTable.vue';
import RepeatersExport from 'components/repeaters/RepeatersExport.vue';
import RepeatersMap from 'components/repeaters/RepeatersMap.vue';

type FactRepeater = components['schemas']['FactRepeater'];
type FactRepeaterResponse =
  paths['/api/v1/repeaters/fact-repeater/']['get']['responses']['200']['content']['application/json'];
type FactRepeaterRequest =
  paths['/api/v1/repeaters/fact-repeater/']['get']['parameters']['query'];

const $q = useQuasar();

const repeaters: Ref<Array<FactRepeater>> = ref([]);
const loading = ref(false);
const tab = ref('list');

watch(loading, (newLoadingValue) => {
  if (newLoadingValue) {
    $q.loadingBar.start();
  } else {
    $q.loadingBar.stop();
  }
});

async function requestRepeaters(
  limit: number,
  offset: number,
  ordering: string | null = null,
): Promise<void> {
  loading.value = true;
  try {
    const response: AxiosResponse<FactRepeaterResponse, FactRepeaterRequest> =
      await api.get('/api/v1/repeaters/fact-repeater/', {
        params: { limit, offset, ordering, modes__active: true },
      });
    // These fields aren't null because this only happens on success
    repeaters.value = response.data.results!;
  } catch (error) {
    console.error(error);
  }
  loading.value = false;
}

onMounted(() => {
  requestRepeaters(99999, 0);
});
</script>
