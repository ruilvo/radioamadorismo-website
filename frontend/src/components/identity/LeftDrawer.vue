<template>
  <q-drawer
    :show-if-above="defaultToOpen && leftDrawerOpen"
    v-model="leftDrawerOpen"
    side="left"
    bordered
    :breakpoint="breakpoint"
  >
    <q-list>
      <StartPageItem />
      <q-separator key="sep-home-from-pages" />
      <PagesItem />
      <q-separator key="sep-pages-from-api" />
      <ApiItem />
      <q-separator key="end" />
    </q-list>
  </q-drawer>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import { useQuasar } from 'quasar';

import StartPageItem from './left_drawer/StartPageItem.vue';
import PagesItem from './left_drawer/PagesItem.vue';
import ApiItem from './left_drawer/ApiItem.vue';

const props = defineProps({
  modelValue: Boolean,
});

const emits = defineEmits(['update:modelValue']);

const leftDrawerOpen = computed({
  get: () => props.modelValue,
  set: (val) => {
    emits('update:modelValue', val);
  },
});

const $q = useQuasar();

const breakpoint: number = 1023; //  Default breakpoint for QDrawer

const defaultToOpen =
  $q.platform.is.desktop === true && $q.screen.width > breakpoint;
</script>
