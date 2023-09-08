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
      <q-separator />
      <h3>Listagem de repetidores</h3>
      <RepeatersTable :repeaters="repeaters" />
      <q-separator />
      <h3>Exportação <i>(Codeplug)</i></h3>
      <RepeatersExport />
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

type FactRepeater = components['schemas']['FactRepeater'];
type FactRepeaterResponse =
  paths['/api/v1/repeaters/fact-repeater/']['get']['responses']['200']['content']['application/json'];
type FactRepeaterRequest =
  paths['/api/v1/repeaters/fact-repeater/']['get']['parameters']['query'];

const $q = useQuasar();

const repeaters: Ref<Array<FactRepeater>> = ref([]);
const loading = ref(false);

watch(loading, (newLoadingValue) => {
  if (newLoadingValue) {
    $q.loadingBar.start();
  } else {
    $q.loadingBar.stop();
  }
});

async function requestRepeaters(
  ordering: string | null = null,
  step = 10,
): Promise<void> {
  var count = step;
  var limit = count;
  var offset = 0;
  loading.value = true;
  while (count > repeaters.value.length) {
    try {
      const response: AxiosResponse<FactRepeaterResponse, FactRepeaterRequest> =
        await api.get('/api/v1/repeaters/fact-repeater/', {
          params: { limit, offset, ordering, modes__active: true },
        });
      // These fields aren't null because this only happens on success
      repeaters.value.push(...response.data.results!);
      count = response.data.count!;
      offset += step;
    } catch (error) {
      console.error(error);
      break;
    }
  }
  loading.value = false;
}

onMounted(() => {
  requestRepeaters();
});
</script>
