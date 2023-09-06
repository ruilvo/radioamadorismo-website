<template>
  <h3>Informação DMR</h3>
  <q-markup-table>
    <thead>
      <th class="text-center">TG local</th>
      <th class="text-center text-center">Colour Code (C.C.)</th>
      <th class="text-center">Configuração das TSs</th>
    </thead>
    <tbody>
      <tr>
        <td class="text-center">
          {{ props.info_dmr.tg.id }} ({{ props.info_dmr.tg.name }})
        </td>
        <td class="text-center">
          {{ props.info_dmr.color_code }}
        </td>
        <td class="text-center">
          {{ props.info_dmr.ts_configuration }}
        </td>
      </tr>
    </tbody>
  </q-markup-table>
</template>

<script setup lang="ts">
import { components } from 'src/types/api';

type DimDmr = components['schemas']['DimDmr'];

const props = defineProps({
  info_dmr: {
    type: Object as () => DimDmr,
    required: true,
  },
});
</script>
