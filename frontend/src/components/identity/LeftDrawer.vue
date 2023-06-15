<template>
  <q-drawer
    v-model="leftDrawerOpen"
    show-if-above
    side="left"
    bordered
    class="scroll bg-grey-3"
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

<script lang="ts">
import { defineComponent, computed } from 'vue';

import StartPageItem from './left_drawer/StartPageItem.vue';
import PagesItem from './left_drawer/PagesItem.vue';
import ApiItem from './left_drawer/ApiItem.vue';

export default defineComponent({
  name: 'LeftDrawer',
  components: {
    StartPageItem,
    PagesItem,
    ApiItem,
  },
  props: {
    modelValue: Boolean,
  },
  emits: ['update:modelValue'],
  setup(props, { emit }) {
    const leftDrawerOpen = computed({
      get: () => props.modelValue,
      set: (val) => {
        emit('update:modelValue', val);
      },
    });

    return {
      leftDrawerOpen,
    };
  },
});
</script>
