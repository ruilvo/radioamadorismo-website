<template>
  <h3>Informação Fusion/C4FM</h3>
  <q-markup-table>
    <thead>
      <th class="text-center text-italic">Room ID</th>
      <th class="text-center text-italic">Wires-X</th>
    </thead>
    <tbody>
      <tr>
        <td class="text-center">
          {{
            props.info_fusion.room_id == ''
              ? '«desconhecido»'
              : props.info_fusion.room_id
          }}
        </td>
        <td class="text-center">
          {{
            props.info_fusion.wiresx == ''
              ? '«desconhecido»'
              : props.info_fusion.wiresx
          }}
        </td>
      </tr>
    </tbody>
  </q-markup-table>
</template>

<script setup lang="ts">
import { components } from 'src/types/api';

type DimFusion = components['schemas']['DimFusion'];

const props = defineProps({
  info_fusion: {
    type: Object as () => DimFusion,
    required: true,
  },
});
</script>
