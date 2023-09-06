<template>
  <div class="q-gutter-y-md">
    <h3>Informação RF</h3>
    <q-markup-table>
      <thead>
        <th class="text-center">Frequência Tx</th>
        <th class="text-center">Frequência Rx</th>
        <th class="text-center text-italic">Shift</th>
      </thead>
      <tbody>
        <tr>
          <td class="text-center">
            {{ format_decimal_field(props.info_rf.tx_mhz!) }}
          </td>
          <td class="text-center">
            {{ format_decimal_field(props.info_rf.rx_mhz!) }}
          </td>
          <td class="text-center text-italic">
            {{ format_decimal_field(props.info_rf.shift_mhz!) }}
          </td>
        </tr>
      </tbody>
    </q-markup-table>
  </div>
</template>

<script setup lang="ts">
import { components } from 'src/types/api';

import { format_decimal_field } from 'src/functions/repeaters';

type DimRf = components['schemas']['DimRf'];

const props = defineProps({
  info_rf: {
    type: Object as () => DimRf,
    required: true,
  },
});
</script>
