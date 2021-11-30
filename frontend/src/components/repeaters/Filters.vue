<template>
  <div class="text-center">
    <h4>Filtros</h4>
  </div>

  <label for="mode-filter">Modo</label>
  <select class="form-select" multiple v-model="selectedModes">
    <option value="fm">FM</option>
    <option value="dstar">D-STAR</option>
    <option value="fusion">Fusion/C4FM</option>
    <option value="dmr">DMR</option>
  </select>
</template>

<script>
import state from "../../shared/repeaters.js";

export default {
  name: "Filters",
  data() {
    return {
      selectedModes: [],
    };
  },

  mounted() {
    state.getRepeaters();
  },
};
</script>
