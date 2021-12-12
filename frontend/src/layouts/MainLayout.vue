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
        </q-list>
      </q-scroll-area>
    </q-drawer>

    <!-- <q-drawer
      v-model="drawer"
      show-if-above


      bordered
      class="bg-grey-3"
    >
    </q-drawer> -->

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
      menuList: [
        {
          icon: "inbox",
          label: "Inbox",
          separator: true,
        },
        {
          icon: "send",
          label: "Outbox",
          separator: false,
        },
        {
          icon: "delete",
          label: "Trash",
          separator: false,
        },
        {
          icon: "error",
          label: "Spam",
          separator: true,
        },
        {
          icon: "settings",
          label: "Settings",
          separator: false,
        },
        {
          icon: "feedback",
          label: "Send Feedback",
          separator: false,
        },
        {
          icon: "help",
          iconColor: "primary",
          label: "Help",
          separator: false,
        },
      ],
    };
  },
  methods: {
    toggleLeftDrawer() {
      this.leftDrawerOpen = !this.leftDrawerOpen;
    },
  },
};
</script>
