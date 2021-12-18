<template>
  <q-page class="column no-wrap" :style-fn="pageStyleFn">
    <div class="col row">
      <div
        class="col-xs-12 col-sm-auto full-height column no-wrap"
        style="width: 300px"
      >
        <RepeatersFilter />
      </div>
      <div class="col-xs-12 col-sm full-height column no-wrap scroll">
        <router-view />
      </div>
    </div>
  </q-page>
</template>

<script>
import { useQuasar } from "quasar";

import RepeatersFilter from "src/components/repeaters/RepeatersFilter";

export default {
  name: "Repeaters",
  components: {
    RepeatersFilter,
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
};
</script>
