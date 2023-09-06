<template>
  <h3>Informação FM</h3>
  <q-markup-table>
    <thead>
      <th class="text-center">Modulação</th>
      <th class="text-center">Tom</th>
    </thead>
    <tbody>
      <tr>
        <td class="text-center">
          {{ props.info_fm.modulation! }}
        </td>
        <td class="text-center">
          {{ format_decimal_field(props.info_fm.tone!, 1) }}
        </td>
      </tr>
    </tbody>
  </q-markup-table>
</template>

<script setup lang="ts">
import { components } from 'src/types/api';

import { format_decimal_field } from 'src/functions/repeaters';

type DimFm = components['schemas']['DimFm'];

const props = defineProps({
  info_fm: {
    type: Object as () => DimFm,
    required: true,
  },
});
</script>
