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
      <q-separator key="sep-home-from-rest" />
    </q-list>
  </q-drawer>
</template>

<script lang="ts">
import { defineComponent, computed } from 'vue';

import StartPageItem from './left_drawer/StartPageItem.vue';

export default defineComponent({
  name: 'LeftDrawer',
  components: {
    StartPageItem,
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
