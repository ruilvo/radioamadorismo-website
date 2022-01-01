<template>
  <q-page padding>
    <h2>Repetidores</h2>
    <div class="overflow-auto">
      <div class="row q-gutter-sm">
        <div class="col-xs-12 col-sm-auto">
          <RepeatersFilters />
        </div>
        <div class="col-xs-12 col-sm">
          <router-view />
        </div>
      </div>
    </div>
  </q-page>
</template>

<script>
import { defineComponent } from "vue";

import RepeatersFilters from "components/RepeatersFilters";

export default defineComponent({
  name: "Repeaters",
  components: {
    RepeatersFilters,
  },
});
</script>
