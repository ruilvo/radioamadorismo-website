<template>
  <h3>Informação da Associação</h3>
  <q-markup-table>
    <thead>
      <th class="text-center">Abreviatura</th>
      <th class="text-center">Nome</th>
      <th class="text-center">Correio eletrónico</th>
      <th class="text-center">Sítio na Internet</th>
    </thead>
    <tbody>
      <tr>
        <td class="text-center">
          {{ props.info_holder.abrv }}
        </td>
        <td class="text-center">
          {{ props.info_holder.name }}
        </td>
        <td class="text-center">
          <a :href="'mailto:' + props.info_holder.email">{{
            props.info_holder.email
          }}</a>
        </td>
        <td class="text-center">
          <a :href="props.info_holder.website">{{
            props.info_holder.website
          }}</a>
        </td>
      </tr>
    </tbody>
  </q-markup-table>
</template>

<script setup lang="ts">
import { components } from 'src/types/api';

type Association = components['schemas']['Association'];

const props = defineProps({
  info_holder: {
    type: Object as () => Association,
    required: true,
  },
});
</script>
