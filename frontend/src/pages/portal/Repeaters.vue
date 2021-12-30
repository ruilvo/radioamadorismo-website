<template>
  <q-page class="row" :style-fn="pageStyleFn">
    <div
      class="col-xs-12 col-sm-shrink full-height column no-wrap"
      style="min-width: 300px"
    >
      <Filter />
    </div>
    <div class="col-xs-12 col-sm full-height column no-wrap scroll">
      <router-view />
    </div>
  </q-page>
</template>

<script>
import { defineComponent } from "vue";
import { useQuasar } from "quasar";

import Filter from "components/portal/repeaters/Filter";

export default defineComponent({
  name: "Repeaters",
  components: {
    Filter,
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
