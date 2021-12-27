<template>
  <q-expansion-item
    key="repeaters-item"
    v-model="repeaters_expanded"
    expand-separator
    icon="cell_tower"
    to="/repetidores"
    label="Repetidores"
  >
    <q-item
      key="repeaters-list-item"
      clickable
      to="/repetidores"
      exact
      :inset-level="1"
    >
      <q-item-section avatar>
        <q-icon name="list" />
      </q-item-section>
      <q-item-section>Lista</q-item-section>
    </q-item>
    <q-item
      key="repeaters-map-item"
      clickable
      to="/repetidores/mapa"
      :inset-level="1"
    >
      <q-item-section avatar>
        <q-icon name="map" />
      </q-item-section>
      <q-item-section>Mapa</q-item-section>
    </q-item>
  </q-expansion-item>
</template>

<script>
import { defineComponent, ref, watch } from "vue";

import { useRoute } from "vue-router";

export default defineComponent({
  name: "RepeatersItem",
  setup() {
    const $route = useRoute();

    const repeaters_expanded = ref($route.path.includes("/repetidores"));

    watch($route, (to) => {
      if (to.path.includes("/repetidores")) {
        repeaters_expanded.value = true;
      }
    });

    return {
      repeaters_expanded,
    };
  },
});
</script>
