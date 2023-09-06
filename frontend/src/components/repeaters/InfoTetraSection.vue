<template>
  <h3>Informação TETRA</h3>
  <q-markup-table>
    <thead>
      <th class="text-center">MCC</th>
      <th class="text-center">MNC</th>
    </thead>
    <tbody>
      <tr>
        <td class="text-center">
          {{ props.info_tetra.mcc }}
        </td>
        <td class="text-center">
          {{ props.info_tetra.mnc }}
        </td>
      </tr>
    </tbody>
  </q-markup-table>
</template>

<script setup lang="ts">
import { components } from 'src/types/api';

type DimTetra = components['schemas']['DimTetra'];

const props = defineProps({
  info_tetra: {
    type: Object as () => DimTetra,
    required: true,
  },
});
</script>
