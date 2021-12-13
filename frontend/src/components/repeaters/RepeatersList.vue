<template>
  {{ this.repeatersStore.repeaters }}
</template>

<script>
import { mapStores } from "pinia";
import { useRepeatersStore } from "src/stores/repeaters";

export default {
  name: "RepeatersList",
  mounted() {
    this.repeatersStore.updateRepeaters();
  },
  computed: {
    // mapStores produces an object called [id]Store...
    ...mapStores(useRepeatersStore), // aka this.repeatersStore
  },
};
</script>
