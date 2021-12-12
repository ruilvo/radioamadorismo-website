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
          <q-item clickable v-ripple to="/" key="start" exact>
            <q-item-section avatar>
              <q-icon name="home" />
            </q-item-section>
            <q-item-section>Página inicial</q-item-section>
          </q-item>
          <q-separator key="sep1" />
          <q-item clickable v-ripple key="repeaters" to="/repetidores">
            <q-item-section avatar>
              <q-icon name="room" />
            </q-item-section>
            <q-item-section>Repetidores</q-item-section>
          </q-item>
          <q-item
            inset-level="1"
            v-if="currentRoutePath.includes('/repetidores')"
            key="repeaters-menu"
          >
            <q-list>
              <q-item
                clickable
                v-ripple
                to="/repetidores"
                key="repeaters-menu-list"
              >
                <q-item-section>Lista</q-item-section>
              </q-item>
              <q-item clickable v-ripple key="repeaters-menu-map">
                <q-item-section>Mapa</q-item-section>
              </q-item>
            </q-list>
          </q-item>

          <!--
          <template v-for="(menuItem, index) in menuList" :key="index">
            <q-item clickable :active="menuItem.label === 'Outbox'" v-ripple>
              <q-item-section avatar>
                <q-icon :name="menuItem.icon" />
              </q-item-section>
              <q-item-section>
                {{ menuItem.label }}
              </q-item-section>
            </q-item>
            <q-separator :key="'sep' + index" v-if="menuItem.separator" />
          </template>
          -->
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
};
</script>
