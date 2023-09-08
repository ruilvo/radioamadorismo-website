<template>
  <div class="row">
    <q-table
      :rows="props.repeaters"
      :columns="columns"
      no-data-label="Sem dados para apresentar"
      no-results-label="Sem resultados para apresentar"
      row-key="id"
      class="col-12"
    >
      <template v-slot:header="props">
        <q-tr>
          <!--  First row of the header -->
          <q-th :props="props" key="callsign" rowspan="2">Indicativo</q-th>
          <q-th colspan="3" class="text-center">Localização</q-th>
          <q-th colspan="2" class="text-center">Entidade</q-th>
          <q-th colspan="2" class="text-center">RF</q-th>
          <q-th :props="props" key="modes" rowspan="2">Modos</q-th>
        </q-tr>
        <q-tr>
          <!--  Second row of the header -->

          <!--  Info - location -->
          <q-th :props="props" key="info_location__region">Região</q-th>
          <q-th :props="props" key="info_location__place">Local</q-th>
          <q-th :props="props" key="info_location__qth_loc">QTH loc.</q-th>

          <!--  Info - holder -->
          <q-th :props="props" key="info_holder__abrv">Abrv.</q-th>
          <q-th :props="props" key="info_holder__name">Nome</q-th>

          <!--  Info - RF -->
          <q-th :props="props" key="info_rf__tx_mhz">Tx (MHz)</q-th>
          <q-th :props="props" key="info_rf__rx_mhz">Rx (MHz)</q-th>
        </q-tr>
      </template>

      <template v-slot:body-cell-callsign="props">
        <q-td :props="props">
          <router-link
            :to="{ name: 'repeater_detail', params: { id: props.row.id } }"
          >
            {{ props.row.callsign }}
          </router-link>
        </q-td>
      </template>
    </q-table>
  </div>
</template>

<script setup lang="ts">
import { QTableProps } from 'quasar';

import { components } from 'src/types/api';

import {
  format_decimal_field,
  format_modes_field,
  format_region_field,
} from 'src/functions/repeaters';

type FactRepeater = components['schemas']['FactRepeater'];

const props = defineProps({
  repeaters: {
    type: Array as () => FactRepeater[],
    required: true,
  },
});

const columns: QTableProps['columns'] = [
  {
    name: 'callsign',
    label: 'Indicativo',
    field: 'callsign',
    align: 'center',
    sortable: true,
  },
  {
    name: 'info_location__region',
    label: 'Local',
    field: (repeater: FactRepeater) => {
      if (repeater.info_location != null) {
        // On reading, this field is never null
        return format_region_field(repeater.info_location.region!);
      }
      return '';
    },
    align: 'center',
    sortable: true,
  },
  {
    name: 'info_location__place',
    label: 'Local',
    field: (repeater: FactRepeater) => {
      if (repeater.info_location != null) {
        return repeater.info_location.place;
      }
      return '';
    },
    align: 'center',
    sortable: true,
  },
  {
    name: 'info_location__qth_loc',
    label: 'QTH loc.',
    field: (repeater: FactRepeater) => {
      if (repeater.info_location != null) {
        return repeater.info_location.qth_loc;
      }
      return '';
    },
    align: 'center',
    sortable: true,
  },
  {
    name: 'info_holder__abrv',
    label: 'Abrv.',
    field: (repeater: FactRepeater) => {
      if (repeater.info_holder != null) {
        return repeater.info_holder.abrv;
      }
      return '';
    },
    align: 'center',
    sortable: true,
  },
  {
    name: 'info_holder__name',
    label: 'Nome',
    field: (repeater: FactRepeater) => {
      if (repeater.info_holder != null) {
        return repeater.info_holder.name;
      }
      return '';
    },
    align: 'center',
    sortable: true,
  },
  {
    name: 'info_rf__tx_mhz',
    label: 'Tx (MHz)',
    field: (repeater: FactRepeater) => {
      if (repeater.info_rf != null) {
        return format_decimal_field(repeater.info_rf.tx_mhz);
      }
      return '';
    },
    align: 'center',
    sortable: true,
  },
  {
    name: 'info_rf__rx_mhz',
    label: 'Rx (MHz)',
    field: (repeater: FactRepeater) => {
      if (repeater.info_rf != null) {
        return format_decimal_field(repeater.info_rf.rx_mhz);
      }
      return '';
    },
    align: 'center',
    sortable: true,
  },
  {
    name: 'modes',
    label: 'Modos',
    field: (repeater: FactRepeater) => {
      return format_modes_field(repeater.modes);
    },
    align: 'center',
  },
];
</script>
