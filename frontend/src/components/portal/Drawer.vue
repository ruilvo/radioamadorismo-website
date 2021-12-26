<template>
  <q-drawer
    v-model="leftDrawerOpen"
    show-if-above
    side="left"
    bordered
    class="bg-grey-3"
  >
    <q-list>
      <q-item key="start" clickable to="/" exact>
        <q-item-section avatar>
          <q-icon name="home" />
        </q-item-section>
        <q-item-section>Página inicial</q-item-section>
      </q-item>
      <q-separator key="sep1" />
      <q-expansion-item
        key="repeaters"
        v-model="repeaters_expanded"
        expand-separator
        icon="cell_tower"
        to="/repetidores"
        label="Repetidores"
      >
        <q-item
          key="repeaters-list"
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
          key="repeaters-map"
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
      <q-separator key="sep2" />
      <q-expansion-item
        key="api-tab"
        v-model="api_expanded"
        expand-separator
        icon="api"
        label="API"
      >
        <q-item key="swagger-ui" clickable to="/swagger" exact :inset-level="1">
          <q-item-section avatar>
            <q-icon name="description" />
          </q-item-section>
          <q-item-section>Documentação (🇬🇧)</q-item-section>
        </q-item>
        <q-item
          key="repeaters-api"
          clickable
          tag="a"
          href="/api/v1/repeaters/"
          exact
          :inset-level="1"
        >
          <q-item-section avatar>
            <q-icon name="cell_tower" />
          </q-item-section>
          <q-item-section>Repetidores (🇬🇧)</q-item-section>
          <q-item-section side
            ><q-icon name="launch" size="xs"
          /></q-item-section>
        </q-item>
      </q-expansion-item>
      <q-item key="about-url" clickable to="/sobre">
        <q-item-section avatar>
          <q-icon name="help_outline" />
        </q-item-section>
        <q-item-section>Sobre</q-item-section>
      </q-item>
    </q-list>
  </q-drawer>
</template>

<script>
import { defineComponent, watch, ref, computed } from "vue";

import { useRoute } from "vue-router";

export default defineComponent({
  name: "Drawer",
  props: {
    modelValue: Boolean,
  },
  emits: ["update:modelValue"],
  setup(props, { emit }) {
    const $route = useRoute();

    const repeaters_expanded = ref($route.path.includes("/repetidores"));
    const api_expanded = ref($route.path.includes("/swagger"));

    const leftDrawerOpen = computed({
      get: () => props.modelValue,
      set: (val) => {
        emit("update:modelValue", val);
      },
    });

    watch($route, (to) => {
      if (to.path.includes("/repetidores")) {
        repeaters_expanded.value = true;
      }
      if (to.path.includes("/swagger")) {
        api_expanded.value = true;
      }
    });

    return {
      leftDrawerOpen,
      repeaters_expanded,
      api_expanded,
    };
  },
});
</script>
