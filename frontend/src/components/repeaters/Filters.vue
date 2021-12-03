<template>
  <div class="text-center">
    <h4>Filtros</h4>
  </div>

  <form @submit.prevent="submitFilters">
    <div class="mb-3">
      <label for="region-filter">Região</label>
      <select
        class="form-select"
        multiple
        v-model="selectedRegions"
        id="region-filter"
      >
        <option value="CPT">Continente</option>
        <option value="AZR">Açores</option>
        <option value="MDA">Madeira</option>
        <option value="OT">Outros</option>
      </select>
    </div>

    <div class="mb-3">
      <label for="mode-filter">Modo</label>
      <select
        class="form-select"
        multiple
        v-model="selectedModes"
        id="mode-filter"
      >
        <option value="fm">FM</option>
        <option value="dstar">D-STAR</option>
        <option value="fusion">Fusion/C4FM</option>
        <option value="dmr">DMR</option>
      </select>
    </div>

    <div class="mb-3">
      <label for="band-filter">Freq.</label>
      <div class="input-group" id="band-filter">
        <input
          type="number"
          step="any"
          class="form-control"
          v-model="minFreq"
        />
        <span class="input-group-addon">-</span>
        <input
          type="number"
          step="any"
          class="form-control"
          v-model="maxFreq"
        />
      </div>
    </div>

    <div class="mb-3">
      <button type="submit" class="btn btn-primary mb-3" onclick="this.blur();">
        Submeter
      </button>
    </div>
  </form>
</template>

<script>
import state from "../../shared/repeaters.js";

export default {
  name: "Filters",
  data() {
    return {
      selectedRegions: ["CPT", "AZR", "MDA"],
      selectedModes: ["fm", "dstar", "fusion", "dmr"],
      minFreq: 144.0,
      maxFreq: 440.0,
    };
  },

  mounted() {
    this.updateDataFromRouter();
    this.updateQueryFromData();
    state.updateRepeaters();
  },

  beforeUnmount() {
    state.query = {};
    state.repeaters = [];
  },

  methods: {
    updateQueryFromData() {
      state.query = {
        region: this.selectedRegions.join(","),
        mode: this.selectedModes.join(","),
        freq_mhz__gte: this.minFreq,
        freq_mhz__lte: this.maxFreq,
      };
    },
    updateDataFromRouter() {
      this.selectedRegions = [].concat(
        this.$route.query.region || this.selectedRegions
      );
      this.selectedModes = [].concat(
        this.$route.query.mode || this.selectedModes
      );
      this.minFreq = this.$route.query.freq_mhz__gte || this.minFreq;
      this.maxFreq = this.$route.query.freq_mhz__lte || this.maxFreq;
    },
    updateRouteFromQuery() {
      this.$router.push({
        query: state.query,
      });
    },
    submitFilters() {
      this.updateQueryFromData();
      this.updateRouteFromQuery();
      state.updateRepeaters();
    },
  },
};
</script>
