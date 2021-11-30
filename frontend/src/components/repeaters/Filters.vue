<template>
  <div class="text-center">
    <h4>Filtros</h4>
  </div>

  <label for="mode-filter">Modo</label>
  <select
    class="form-select"
    multiple
    @change="handleModeFilter"
    id="mode-filter"
    ref="mode-filter"
  >
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

  mounted() {
    state.getRepeaters();
  },

  methods: {
    handleModeFilter() {
      const selectedOptions = [...this.$refs["mode-filter"].selectedOptions];
      const selectedValues = selectedOptions.map((option) => option.value);
      console.log(selectedValues);
    },
  },
};
</script>
