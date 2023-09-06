<template>
  <div class="row">
    <q-table
      :rows="repeaters"
      :columns="columns"
      :loading="loading"
      v-model:pagination="pagination"
      @request="onRequest"
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
          <a :href="'/api/v1/repeaters/fact-repeater/' + props.row.id">{{
            props.row.callsign
          }}</a>
        </q-td>
      </template>
    </q-table>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, Ref } from 'vue';
import { api } from 'boot/axios';

import { AxiosResponse } from 'axios';

import { paths, components } from 'src/types/api';

import {
  format_decimal_field,
  format_modes_field,
  format_region_field,
} from 'src/functions/repeaters';

type FactRepeater = components['schemas']['FactRepeater'];
type FactRepeaterResponse =
  paths['/api/v1/repeaters/fact-repeater/']['get']['responses']['200']['content']['application/json'];
type FactRepeaterRequest =
  paths['/api/v1/repeaters/fact-repeater/']['get']['parameters']['query'];

const loading = ref(false);

interface Pagination {
  page: number;
  rowsPerPage: number;
  rowsNumber: number;
  sortBy: string | null;
  descending: boolean;
}

const pagination: Ref<Pagination> = ref({
  page: 1,
  rowsPerPage: 10,
  rowsNumber: 10,
  sortBy: null,
  descending: false,
});

const repeaters: Ref<Array<FactRepeater>> = ref([]);

async function requestRepeaters(
  limit: number,
  offset: number,
  ordering: string | null = null,
): Promise<void> {
  loading.value = true;
  try {
    const response: AxiosResponse<FactRepeaterResponse, FactRepeaterRequest> =
      await api.get('/api/v1/repeaters/fact-repeater/', {
        params: { limit, offset, ordering },
      });
    // These fields aren't null because this only happens on success
    repeaters.value = response.data.results!;
    pagination.value.rowsNumber = response.data.count!;
  } catch (error) {
    console.error(error);
  }
  loading.value = false;
}

function onRequest(requestProp: {
  pagination: {
    sortBy: string;
    descending: boolean;
    page: number;
    rowsPerPage: number;
  };
  /* eslint-disable @typescript-eslint/no-explicit-any */
  filter?: any;
  getCellValue: (col: any, row: any) => any;
  /* eslint-enable @typescript-eslint/no-explicit-any */
}): void {
  const { page, rowsPerPage, sortBy, descending } = requestProp.pagination;
  console.log(sortBy, descending);
  var limit = rowsPerPage;
  if (limit === 0) {
    limit = pagination.value.rowsNumber;
  }
  const offset = (page - 1) * limit;
  var ordering = null;
  if (sortBy != null) {
    ordering = sortBy;
    if (descending) {
      ordering = `-${ordering}`;
    }
  }
  requestRepeaters(limit, offset, ordering);
  pagination.value.page = page;
  pagination.value.rowsPerPage = rowsPerPage;
  pagination.value.sortBy = sortBy;
  pagination.value.descending = descending;
}

onMounted(() => {
  const limit = pagination.value.rowsPerPage;
  const offset = (pagination.value.page - 1) * limit;
  requestRepeaters(limit, offset);
});

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
