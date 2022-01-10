<template>
  <div class="column full-height">
    <h2 class="col-auto" style="margin-bottom: 15px">
      Base de dados de repetidores
    </h2>
    <div class="col">
      <div class="row full-height q-col-gutter-md">
        <div class="col-xs-12 col-sm-auto"><RepeatersFilters /></div>
        <div class="col">
          <router-view />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { defineComponent } from "vue";

import RepeatersFilters from "components/repeaters/RepeatersFilters.vue";

export default defineComponent({
  name: "Repeaters",
  components: {
    RepeatersFilters,
  },
});
</script>
