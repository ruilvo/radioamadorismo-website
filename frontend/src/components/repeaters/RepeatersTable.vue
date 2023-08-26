<template>
  <h3>Listagem de repetidores</h3>
  <div class="row">
    <q-table :data="repeaters" :columns="columns" row-key="id" class="col-12">
      <template v-slot:header="props">
        <q-tr>
          <!--  First row of the header -->
          <q-td :props="props" key="callsign" rowspan="2">Indicativo</q-td>
          <q-td colspan="3">Localização</q-td>
          <q-td colspan="2">Entidade</q-td>
          <q-td colspan="2">RF</q-td>
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

const columns = [
  {
    name: 'callsign',
    label: 'Indicativo',
    field: 'callsign',
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
  },
  {
    name: 'info_rf__tx_mhz',
    label: 'Tx (MHz)',
    field: (repeater: FactRepeater) => {
      if (repeater.info_rf != null) {
        return repeater.info_rf.tx_mhz;
      }
      return '';
    },
  },
  {
    name: 'info_rf__rx_mhz',
    label: 'Rx (MHz)',
    field: (repeater: FactRepeater) => {
      if (repeater.info_rf != null) {
        return repeater.info_rf.rx_mhz;
      }
      return '';
    },
  },
];
</script>
