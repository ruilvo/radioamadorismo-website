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
      <label for="band-filter">Banda</label>
      <select
        class="form-select"
        multiple
        v-model="selectedBands"
        id="band-filter"
      >
        <option value="g2m">&gt; 2m</option>
        <option value="2m">2m</option>
        <option value="70cm">70cm</option>
        <option value="l70cm">&lt; 70cm</option>
      </select>
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
      selectedBands: ["2m", "70cm"],
    };
  },

  mounted() {
    state.getRepeaters();
  },

  methods: {
    submitFilters() {
      console.log("Submited!");
    },
  },
};
</script>
