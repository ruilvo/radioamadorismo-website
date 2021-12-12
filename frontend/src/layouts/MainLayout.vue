<template>
  <q-layout view="hhh lpr fff">
    <q-header bordered class="bg-primary text-white">
      <q-toolbar>
        <q-btn dense flat round icon="menu" @click="toggleLeftDrawer" />

        <q-toolbar-title>
          <span class="text-italic q-mr-sm">Æ</span>
          <span class="q-mr-sm">Portal do Radioamadorismo</span>
          <span class="text-caption">Um projeto de Rui "CT7ALW" Oliveira</span>
        </q-toolbar-title>
      </q-toolbar>
    </q-header>

    <q-drawer
      show-if-above
      v-model="leftDrawerOpen"
      side="left"
      bordered
      class="bg-grey-3"
      :width="200"
      :breakpoint="500"
    >
      <q-scroll-area class="fit">
        <q-list>
          <q-item clickable to="/" key="start" exact>
            <q-item-section avatar>
              <q-icon name="home" />
            </q-item-section>
            <q-item-section>Página inicial</q-item-section>
          </q-item>
          <q-separator key="sep1" />
          <q-expansion-item
            expand-separator
            icon="room"
            key="repeaters"
            to="/repetidores"
            label="Repetidores"
            v-model="repeaters_expanded"
          >
            <q-item
              clickable
              to="/repetidores"
              exact
              key="repeaters-list"
              :inset-level="1"
            >
              <q-item-section>Lista</q-item-section>
            </q-item>
            <q-item
              clickable
              to="/repetidores/mapa"
              key="repeaters-map"
              :inset-level="1"
            >
              <q-item-section>Mapa</q-item-section>
            </q-item>
          </q-expansion-item>
          <q-separator key="sep2" />
          <q-item clickable key="api-url">
            <q-item-section avatar>
              <q-icon name="api" />
            </q-item-section>
            <q-item-section>API</q-item-section>
          </q-item>
          <q-item clickable key="about-url">
            <q-item-section avatar>
              <q-icon name="help_outline" />
            </q-item-section>
            <q-item-section>Sobre</q-item-section>
          </q-item>
        </q-list>
      </q-scroll-area>
    </q-drawer>

    <q-page-container>
      <router-view />
    </q-page-container>
  </q-layout>
</template>

<script>
export default {
  name: "MainLayout",
  data() {
    return {
      leftDrawerOpen: false,
      repeaters_expanded: this.$route.path.includes("/repetidores"),
    };
  },
  methods: {
    toggleLeftDrawer() {
      this.leftDrawerOpen = !this.leftDrawerOpen;
    },
  },
  computed: {
    currentRoutePath() {
      return this.$route.path;
    },
  },
  watch: {
    currentRoutePath: function (to, from) {
      if (to.includes("/repetidores")) {
        this.repeaters_expanded = true;
      }
    },
  },
};
</script>
