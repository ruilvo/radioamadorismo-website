<template>
  <div class="text-h6">Filtros</div>
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

    <div>
      <q-badge>
        Frequência: {{ freqRange.min }} a {{ freqRange.max }} MHz</q-badge
      >
      <div class="q-mx-md">
        <q-range v-model="freqRange" :min="0" :max="1500" />
      </div>
    </div>

    <div>
      <q-btn label="Submeter" type="submit" color="primary" />
    </div>
  </q-form>
</template>

<script>
import { defineComponent, ref, watch, onUnmounted } from "vue";

import { useRouter, useRoute } from "vue-router";

import useRepeatersStore from "src/stores/repeaters";

import routeMatchesName from "src/scripts/route_matches_name";
import isObjectEmpty from "src/scripts/is_object_empty";

export default defineComponent({
  name: "RepeatersFilters",
  setup() {
    const $router = useRouter();
    const $route = useRoute();

    const repeatersStore = useRepeatersStore();
    onUnmounted(() => {
      repeatersStore.$reset;
    });

    const selectedRegions = ref(["CPT", "AZR", "MDA"]);
    const selectedModes = ref(["fm", "dstar", "fusion", "dmr"]);

    const freqRange = ref({
      min: 144.0,
      max: 440.0,
    });

    function updateDataFromRouter() {
      if ($route.query.region) {
        selectedRegions.value = $route.query.region.split(",");
      }
      if ($route.query.mode) {
        selectedModes.value = $route.query.mode.split(",");
      }
      if ($route.query.freq_mhz__gte) {
        freqRange.value.min = parseFloat($route.query.freq_mhz__gte);
      }
      if ($route.query.freq_mhz__lte) {
        freqRange.value.max = parseFloat($route.query.freq_mhz__lte);
      }
    }

    function updateQueryFromData() {
      repeatersStore.query = {
        region: selectedRegions.value.join(","),
        mode: selectedModes.value.join(","),
        freq_mhz__gte: freqRange.value.min,
        freq_mhz__lte: freqRange.value.max,
      };
    }

    async function updateRepeatersAll() {
      await repeatersStore.updateRepeaters(0, 1);
      await repeatersStore.updateRepeaters(0, repeatersStore.count);
    }

    updateDataFromRouter();
    updateQueryFromData();
    $router.replace({
      query: repeatersStore.query,
    });
    updateRepeatersAll();

    const invalidateRouteWatcher = ref(false);
    watch($route, (newVal, oldVal) => {
      if (invalidateRouteWatcher.value) {
        return;
      }
      if (newVal.query !== oldVal.query) {
        updateDataFromRouter();
      }
      if (newVal.path !== oldVal.path) {
        // This is for us to be able to change between repetidores/ and
        // repetidores/mapa keeping the query intact.
        if (
          routeMatchesName($route, "repeaters") &&
          isObjectEmpty($route.query)
        ) {
          $router.replace({
            query: repeatersStore.query,
          });
        }
      }
    });

    async function submitFilters() {
      invalidateRouteWatcher.value = true;
      updateQueryFromData();
      $router.push({
        query: repeatersStore.query,
      });
      updateRepeatersAll();
      invalidateRouteWatcher.value = false;
    }

    return {
      selectedRegions,
      selectedModes,
      freqRange,
      submitFilters,
    };
  },
});
</script>
