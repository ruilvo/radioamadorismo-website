<template>
  <div class="text-h6">Filtros</div>
  <div class="col column no-wrap scroll">
    <q-form class="q-gutter-md" @submit="submitFilters">
      <q-select
        v-model="selectedRegions"
        filled
        multiple
        map-options
        emit-value
        :options="[
          { label: 'Continente', value: 'CPT' },
          { label: 'Açores', value: 'AZR' },
          { label: 'Madeira', value: 'MDA' },
          { label: 'Outros', value: 'OT' },
        ]"
        label="Região"
      />

      <q-select
        v-model="selectedModes"
        filled
        multiple
        map-options
        emit-value
        :options="[
          { label: 'FM', value: 'fm' },
          { label: 'D-STAR', value: 'dstar' },
          { label: 'Fusion', value: 'fusion' },
          { label: 'DMR', value: 'dmr' },
        ]"
        label="Modos"
      />

      <div class="q-mx-md">
        <q-badge>
          Frequência: {{ freqRange.min }} a {{ freqRange.max }} MHz</q-badge
        >
        <q-range v-model="freqRange" :min="0" :max="1500" />
      </div>
    </q-form>
    <div class="row">
      <q-btn color="primary" label="Submeter" @click="submitFilters" />
    </div>
  </div>
</template>

<script>
import { defineComponent, ref, computed, onUnmounted, watch } from "vue";
import { useRouter, useRoute } from "vue-router";

import useRepeatersStore from "src/stores/repeaters";

function isObjectEmpty(value) {
  return Object.keys(value).length === 0 && value.constructor === Object;
}

export default defineComponent({
  name: "RepeatersFilters",
  setup() {
    const $router = useRouter();
    const $route = useRoute();

    const repeatersStore = useRepeatersStore();

    const selectedRegions = ref(["CPT", "AZR", "MDA"]);
    const selectedModes = ref(["fm", "dstar", "fusion", "dmr"]);
    const freqRange = ref({
      min: 144.0,
      max: 440.0,
    });

    const minFreq = computed({
      get: () => freqRange.value.min,
      set: (val) => {
        freqRange.value.min = val;
      },
    });
    const maxFreq = computed({
      get: () => freqRange.value.max,
      set: (val) => {
        freqRange.value.max = val;
      },
    });

    function updateQueryFromData() {
      repeatersStore.query = {
        region: selectedRegions.value.join(","),
        mode: selectedModes.value.join(","),
        freq_mhz__gte: minFreq.value,
        freq_mhz__lte: maxFreq.value,
      };
    }

    function updateDataFromRouter() {
      if ($route.query.region) {
        selectedRegions.value = $route.query.region.split(",");
      }
      if ($route.query.mode) {
        selectedModes.value = $route.query.mode.split(",");
      }
      minFreq.value = $route.query.freq_mhz__gte || minFreq.value;
      maxFreq.value = $route.query.freq_mhz__lte || maxFreq.value;
    }

    function updateRouteFromQuery() {
      $router.push({
        query: repeatersStore.query,
      });
    }

    function initRouteFromQuery() {
      if (isObjectEmpty($route.query)) {
        $router.replace({
          query: repeatersStore.query,
        });
      }
    }

    function submitFilters() {
      updateQueryFromData();
      updateRouteFromQuery();
      repeatersStore
        .updateRepeaters(0, 1)
        .then(repeatersStore.updateRepeaters(0, repeatersStore.count));
    }

    onUnmounted(() => {
      repeatersStore.$reset;
    });

    updateDataFromRouter();
    updateQueryFromData();
    initRouteFromQuery();
    repeatersStore.updateRepeaters();

    watch($route, () => {
      // Handle navigating from /repetidores to /repetidores/mapa keeping the query
      if ($route.path.includes("/repetidores")) {
        if (isObjectEmpty($route.query)) {
          $router.replace({
            query: repeatersStore.query,
          });
        }
      }
    });

    return { submitFilters, selectedRegions, selectedModes, freqRange };
  },
});
</script>
