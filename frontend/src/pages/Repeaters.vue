<template>
  <q-page padding :style-fn="pageStyleFn">
    <h2>Repetidores</h2>
    <div class="row" style="height: 90%">
      <div class="row q-gutter-sm col">
        <div class="col-xs-12 col-sm-auto">
          <RepeatersFilters />
        </div>
        <div class="row col-xs-12 col-sm column">
          <router-view />
        </div>
      </div>
    </div>
  </q-page>
</template>

<script>
import { defineComponent } from "vue";

import { useQuasar } from "quasar";

import RepeatersFilters from "components/RepeatersFilters";

export default defineComponent({
  name: "Repeaters",
  components: {
    RepeatersFilters,
  },
  setup() {
    const $q = useQuasar();

    return {
      pageStyleFn(offset, height) {
        return {
          [$q.screen.gt.xs ? "height" : "minHeight"]: `${height - offset}px`,
        };
      },
    };
  },
});
</script>
