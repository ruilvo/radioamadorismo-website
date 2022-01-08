<template>
  <div>
    <div class="column full-height">
      <h2 class="col-auto">Repetidores</h2>
      <div class="col row q-gutter-sm">
        <div class="col-xs-12 col-sm-auto">
          <RepeatersFilters />
        </div>
        <div class="row col-xs-12 col-sm">
          <router-view />
        </div>
      </div>
    </div>
  </div>
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
