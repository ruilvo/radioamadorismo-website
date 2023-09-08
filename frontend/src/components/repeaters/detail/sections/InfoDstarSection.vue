<template>
  <h3>Informação D-STAR</h3>
  <q-markup-table>
    <thead>
      <th class="text-center text-italic">Gateway</th>
      <th class="text-center text-italic">Reflector</th>
    </thead>
    <tbody>
      <tr>
        <td class="text-center">
          {{
            props.info_dstar.gateway == ''
              ? '«desconhecido»'
              : props.info_dstar.gateway
          }}
        </td>
        <td class="text-center">
          {{
            props.info_dstar.reflector == ''
              ? '«desconhecido»'
              : props.info_dstar.reflector
          }}
        </td>
      </tr>
    </tbody>
  </q-markup-table>
</template>

<script setup lang="ts">
import { components } from 'src/types/api';

type DimDstar = components['schemas']['DimDstar'];

const props = defineProps({
  info_dstar: {
    type: Object as () => DimDstar,
    required: true,
  },
});
</script>
