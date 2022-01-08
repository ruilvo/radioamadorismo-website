<template>
  <q-expansion-item
    key="repeaters-item"
    v-model="repeaters_expanded"
    expand-separator
    icon="cell_tower"
    :to="{ name: 'repeaters-list' }"
    label="Repetidores"
  >
    <q-item
      key="repeaters-list-item"
      clickable
      :to="{ name: 'repeaters-list' }"
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
      :to="{ name: 'repeaters-map' }"
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

import routeMatchesName from "src/scripts/route_matches_name";

export default defineComponent({
  name: "RepeatersItem",
  setup() {
    const $route = useRoute();

    const repeaters_expanded = ref(routeMatchesName($route, "repeaters"));

    watch($route, () => {
      if (routeMatchesName($route, "repeaters")) {
        repeaters_expanded.value = true;
      }
    });

    return {
      repeaters_expanded,
    };
  },
});
</script>
