<template>
  <q-drawer show-if-above v-model="leftDrawerOpen" side="left" bordered>
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
</script>
