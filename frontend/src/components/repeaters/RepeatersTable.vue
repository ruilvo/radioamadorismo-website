<template>
  <h3>Listagem de repetidores</h3>
  <div class="row">
    <q-table
      :rows="repeaters"
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
          <q-th colspan="2" class="text-center">Localização</q-th>
          <q-th colspan="2" class="text-center">Entidade</q-th>
          <q-th colspan="2" class="text-center">RF</q-th>
          <q-th :props="props" key="modes" rowspan="2">Modos</q-th>
        </q-tr>
        <q-tr>
          <!--  Second row of the header -->

          <!--  Info - location -->
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
    </q-table>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, Ref } from 'vue';
import { api } from 'boot/axios';

import { FactRepeater } from 'src/components/models';

const repeaters: Ref<Array<FactRepeater>> = ref([]);

onMounted(async () => {
  try {
    const response = await api.get('/api/v1/repeaters/fact-repeater/?limit=10');
    repeaters.value = response.data.results;
  } catch (error) {
    console.error(error);
  }
});

function format_rf_field(field: string): string {
  return Number.parseFloat(field).toFixed(4).toString();
}

function format_modes_field(field: Array<string>): string {
  const modeMap: { [key: string]: string } = {
    fm: 'FM',
    dmr: 'DMR',
    dstar: 'D-Star',
    fusion: 'Fusion',
    tetra: 'TETRA',
  };
  const modes_formatted = field.map((mode) => modeMap[mode]);
  return modes_formatted.join(', ');
}

// Generated with copilot
/* eslint-disable @typescript-eslint/no-explicit-any */
interface TableColumn {
  name: string;
  label: string;
  field: string | ((row: FactRepeater) => any);
  required?: boolean;
  align?: 'center' | 'left' | 'right';
  sortable?: boolean;
  sort?: (a: any, b: any, rowA: FactRepeater, rowB: FactRepeater) => number;
  format?: (val: any, row: FactRepeater) => any;
  classes?: string;
  style?: string;
  headerClasses?: string;
  headerStyle?: string;
}
/* eslint-enable @typescript-eslint/no-explicit-any */

const columns: Array<TableColumn> = [
  {
    name: 'callsign',
    label: 'Indicativo',
    field: 'callsign',
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
        return format_rf_field(repeater.info_rf.tx_mhz);
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
        return format_rf_field(repeater.info_rf.rx_mhz);
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
    sortable: true,
  },
];
</script>
