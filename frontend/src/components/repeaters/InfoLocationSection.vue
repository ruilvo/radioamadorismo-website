<template>
  <h3>Informação do Local</h3>
  <q-markup-table>
    <thead>
      <th class="text-center">Região</th>
      <th class="text-center">Local</th>
      <th class="text-center text-italic">QTH (mainhead) locator</th>
      <th class="text-center">Latitude</th>
      <th class="text-center">Longitude</th>
    </thead>
    <tbody>
      <tr>
        <td class="text-center">
          {{ format_region_field(props.info_location.region!) }}
        </td>
        <td class="text-center">
          {{ props.info_location.place }}
        </td>
        <td class="text-center">
          {{ props.info_location.qth_loc }}
        </td>
        <td class="text-center">
          {{ format_decimal_field(props.info_location.latitude!, 6) }}
        </td>
        <td class="text-center">
          {{ format_decimal_field(props.info_location.longitude!, 6) }}
        </td>
      </tr>
    </tbody>
  </q-markup-table>
</template>

<script setup lang="ts">
import { components } from 'src/types/api';

import {
  format_decimal_field,
  format_region_field,
} from 'src/functions/repeaters';

type DimLocation = components['schemas']['DimLocation'];

const props = defineProps({
  info_location: {
    type: Object as () => DimLocation,
    required: true,
  },
});
</script>
