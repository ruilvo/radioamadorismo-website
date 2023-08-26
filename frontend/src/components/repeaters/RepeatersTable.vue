<template>
  <h3>Listagem de repetidores</h3>
</template>

<script setup lang="ts">
import { ref, onMounted, Ref, computed } from 'vue';
import { api } from 'boot/axios';

import { FactRepeater } from 'src/components/models';

const repeaters: Ref<Array<FactRepeater>> = ref([]);

onMounted(async () => {
  try {
    const response = await api.get('/api/v1/repeaters/fact-repeater/?limit=10');
    repeaters.value = response.data.results;
  } catch (error) {
    console.error(error);
  }
});

const repeatersAsTree = computed(() => {
  const tree = repeaters.value.map((repeater) => {
    var children = [];
    if (!(repeater.info_rf === null)) {
      children.push({
        id: repeater.info_rf.id,
        label: repeater.info_rf.tx_mhz,
        children: [],
      });
    }
    return {
      id: repeater.id,
      label: repeater.callsign,
      children: children,
    };
  });
  return tree;
});
</script>
