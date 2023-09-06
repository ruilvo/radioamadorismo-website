<template>
  <h3>Informação do Repetidor</h3>
  <q-markup-table>
    <thead>
      <th class="text-center">Potência (W)</th>
      <th class="text-center">Status</th>
      <th class="text-center text-italic">Sysop</th>
      <th class="text-center">Notas</th>
    </thead>
    <tbody>
      <tr>
        <td class="text-center">{{ props.repeater.pwr_w }}</td>
        <td class="text-center">
          {{ format_status_field(props.repeater.status!) }}
        </td>
        <td class="text-center">
          {{
            props.repeater.sysop == '' ? '«desconhecido»' : props.repeater.sysop
          }}
        </td>
        <td class="text-center">{{ props.repeater.notes }}</td>
      </tr>
    </tbody>
  </q-markup-table>
</template>

<script setup lang="ts">
import { components } from 'src/types/api';

import { format_status_field } from 'src/functions/repeaters';

type FactRepeater = components['schemas']['FactRepeater'];

const props = defineProps({
  repeater: {
    type: Object as () => FactRepeater,
    required: true,
  },
});
</script>
