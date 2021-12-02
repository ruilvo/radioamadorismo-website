<template>
  <div class="text-center">
    <h4>Filtros</h4>
  </div>

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

  <label for="mode-filter">Modo</label>
  <select class="form-select" multiple v-model="selectedModes" id="mode-filter">
    <option value="fm">FM</option>
    <option value="dstar">D-STAR</option>
    <option value="fusion">Fusion/C4FM</option>
    <option value="dmr">DMR</option>
  </select>

  <label for="rf-filter">RF</label>
  <select class="form-select" multiple v-model="selectedRf" id="rf-filter">
    <option value="simplex">Simplex</option>
    <option value="half_duplex">Semi-duplex</option>
  </select>

  <label for="modulation-filter" class="form-label">Modulação</label>
  <input
    type="email"
    class="form-control"
    id="modulation-filter"
    placeholder="Ex.: 11kHzF3E"
    v-model="modulation"
  />

  <label for="freq-filter" class="form-label">Frequência</label>
  <div class="input-group" id="freq-filter">
    <input type="number" class="form-control" />
    <div class="input-group-prepend">
      <span class="input-group-text">-</span>
    </div>
    <input type="number" class="form-control" />
  </div>
</template>

<script>
import state from "../../shared/repeaters.js";

export default {
  name: "Filters",
  data() {
    return {
      selectedRegions: [],
      selectedModes: [],
      selectedRf: [],
      modulation: "",
    };
  },

  mounted() {
    state.getRepeaters();
  },
};
</script>
