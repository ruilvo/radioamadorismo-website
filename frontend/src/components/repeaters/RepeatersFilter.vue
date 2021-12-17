<template>
  <div class="text-h6 q-ml-sm">Filtros</div>
  <div class="q-pa-md" style="max-width: 300px">bananas</div>
</template>

<script>
import { defineComponent, ref, onBeforeMount } from "vue";
import { useRouter, useRoute } from "vue-router";
import { useRepeatersStore } from "src/stores/repeaters";

export default defineComponent({
  name: "RepeatersFilter",
  setup() {
    const $router = useRouter();
    const $route = useRoute();

    const repeatersStore = useRepeatersStore();

    const selectedRegions = ref(["CPT", "AZR", "MDA"]);
    const selectedModes = ref(["fm", "dstar", "fusion", "dmr"]);
    const minFreq = ref(144.0);
    const maxFreq = ref(440.0);

    function updateQueryFromData() {
      repeatersStore.query = {
        region: selectedRegions.value.join(","),
        mode: selectedModes.value.join(","),
        freq_mhz__gte: minFreq.value,
        freq_mhz__lte: maxFreq.value,
      };
    }

    function updateDataFromRouter() {
      selectedRegions.value = [].concat(
        $route.query.region || selectedRegions.value
      );
      selectedModes.value = [].concat($route.query.mode || selectedModes.value);
      minFreq.value = $route.query.freq_mhz__gte || minFreq.value;
      maxFreq.value = $route.query.freq_mhz__lte || maxFreq.value;
    }

    function updateRouteFromQuery() {
      $router.push({
        query: repeatersStore.query,
      });
    }

    function submitFilters() {
      updateQueryFromData();
      updateRouteFromQuery();
      repeatersStore.updateRepeaters();
    }

    onBeforeMount(() => {
      repeatersStore.$reset;
    });

    updateDataFromRouter();
    updateQueryFromData();
    repeatersStore.updateRepeaters();

    return {};
  },
});
</script>
