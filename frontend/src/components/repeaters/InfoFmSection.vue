<template>
  <div class="q-gutter-y-md">
    <h3>Informação RF</h3>
    <q-markup-table>
      <thead>
        <th class="text-center">Modulação</th>
        <th class="text-center">Tom</th>
        <th class="text-center text-italic">Largura de banda</th>
      </thead>
      <tbody>
        <tr>
          <td class="text-center">
            {{ props.info_fm.modulation! }}
          </td>
          <td class="text-center">
            {{ format_rf_field(props.info_fm.tone!) }}
          </td>
          <td class="text-center text-italic">
            {{ props.info_fm.bandwidth! }}
          </td>
        </tr>
      </tbody>
    </q-markup-table>
  </div>
</template>

<script setup lang="ts">
import { components } from 'src/types/api';

type DimFm = components['schemas']['DimFm'];

const props = defineProps({
  info_fm: {
    type: Object as () => DimFm,
    required: true,
  },
});

function format_rf_field(field: string): string {
  return Number.parseFloat(field).toFixed(4).toString();
}
</script>
