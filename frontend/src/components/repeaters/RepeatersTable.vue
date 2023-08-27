<template>
  <h3>Listagem de repetidores</h3>
  <div class="row">
    <q-table :rows="repeaters" :columns="columns" row-key="id" class="col-12">
      <template v-slot:header="props">
        <q-tr>
          <!--  First row of the header -->
          <q-td :props="props" key="callsign" rowspan="2">Indicativo</q-td>
          <q-td colspan="2" class="text-center">Localização</q-td>
          <q-td colspan="2" class="text-center">Entidade</q-td>
          <q-td colspan="2" class="text-center">RF</q-td>
          <q-td :props="props" key="modes" rowspan="2">Modos</q-td>
        </q-tr>
        <q-tr>
          <!--  Second row of the header -->

          <!--  Info - location -->
          <q-td :props="props" key="info_location__place">Local</q-td>
          <q-td :props="props" key="info_location__qth_loc">QTH loc.</q-td>

          <!--  Info - holder -->
          <q-td :props="props" key="info_holder__abrv">Abrv.</q-td>
          <q-td :props="props" key="info_holder__name">Nome</q-td>

          <!--  Info - RF -->
          <q-td :props="props" key="info_rf__tx_mhz">Tx (MHz)</q-td>
          <q-td :props="props" key="info_rf__rx_mhz">Rx (MHz)</q-td>
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

const columns = [
  {
    name: 'callsign',
    label: 'Indicativo',
    field: 'callsign',
    align: 'center',
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
