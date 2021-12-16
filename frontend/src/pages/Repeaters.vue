<template>
  <q-page>
    <div class="row">
      <div class="col-xs-12 col-sm-12 col-md-4"><RepeatersFilter /></div>
      <div class="col-xs-12 col-sm-12 col-md-4"><router-view /></div>
    </div>
  </q-page>
</template>

<script>
import { mapStores } from "pinia";
import { useRepeatersStore } from "src/stores/repeaters";
import RepeatersFilter from "src/components/repeaters/RepeatersFilter";

export default {
  name: "Repeaters",
  mounted() {
    this.repeatersStore.updateRepeaters();
  },
  computed: {
    // mapStores produces an object called [id]Store...
    ...mapStores(useRepeatersStore), // aka this.repeatersStore
  },
  components: {
    RepeatersFilter,
  },
};
</script>
