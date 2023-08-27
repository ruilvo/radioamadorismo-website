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

async function requestRepeaters(limit: number, offset: number): Promise<void> {
  loading.value = true;
  try {
    const response = await api.get(
      `/api/v1/repeaters/fact-repeater/?limit=${limit}&offset=${offset}`,
    );
    repeaters.value = response.data.results;
    pagination.value.rowsNumber = response.data.count;
  } catch (error) {
    console.error(error);
  }
  loading.value = false;
}

function sortRepeaters(rowKey: string, descending: boolean) {
  // TODO(ruilvo, 2023-08-27): In the future, this should be done in the backend
  switch (rowKey) {
    case 'callsign':
      repeaters.value.sort((a, b) => {
        return descending
          ? b.callsign.localeCompare(a.callsign)
          : a.callsign.localeCompare(b.callsign);
      });
      break;
    case 'info_location__place':
      repeaters.value.sort((a, b) => {
        if (a.info_location == null || b.info_location == null) {
          return 0;
        }
        return descending
          ? b.info_location.place.localeCompare(a.info_location.place)
          : a.info_location.place.localeCompare(b.info_location.place);
      });
      break;
    case 'info_location__qth_loc':
      repeaters.value.sort((a, b) => {
        if (a.info_location == null || b.info_location == null) {
          return 0;
        }
        return descending
          ? b.info_location.qth_loc.localeCompare(a.info_location.qth_loc)
          : a.info_location.qth_loc.localeCompare(b.info_location.qth_loc);
      });
      break;
    case 'info_holder__abrv':
      repeaters.value.sort((a, b) => {
        if (a.info_holder == null || b.info_holder == null) {
          return 0;
        }
        return descending
          ? b.info_holder.abrv.localeCompare(a.info_holder.abrv)
          : a.info_holder.abrv.localeCompare(b.info_holder.abrv);
      });
      break;
    case 'info_holder__name':
      repeaters.value.sort((a, b) => {
        if (a.info_holder == null || b.info_holder == null) {
          return 0;
        }
        return descending
          ? b.info_holder.name.localeCompare(a.info_holder.name)
          : a.info_holder.name.localeCompare(b.info_holder.name);
      });
      break;
    case 'info_rf__tx_mhz':
      repeaters.value.sort((a, b) => {
        if (a.info_rf == null || b.info_rf == null) {
          return 0;
        }
        return descending
          ? Number.parseFloat(b.info_rf.tx_mhz) -
              Number.parseFloat(a.info_rf.tx_mhz)
          : Number.parseFloat(a.info_rf.tx_mhz) -
              Number.parseFloat(b.info_rf.tx_mhz);
      });
      break;
    case 'info_rf__rx_mhz':
      repeaters.value.sort((a, b) => {
        if (a.info_rf == null || b.info_rf == null) {
          return 0;
        }
        return descending
          ? Number.parseFloat(b.info_rf.rx_mhz) -
              Number.parseFloat(a.info_rf.rx_mhz)
          : Number.parseFloat(a.info_rf.rx_mhz) -
              Number.parseFloat(b.info_rf.rx_mhz);
      });
      break;
    case 'modes':
      repeaters.value.sort((a, b) => {
        return descending
          ? format_modes_field(b.modes).localeCompare(
              format_modes_field(a.modes),
            )
          : format_modes_field(a.modes).localeCompare(
              format_modes_field(b.modes),
            );
      });
      break;
    default:
      break;
  }
}

function onRequest(props: { pagination: typeof pagination.value }) {
  const { page, rowsPerPage, sortBy, descending } = props.pagination;
  console.log(sortBy, descending);
  var limit = rowsPerPage;
  if (limit === 0) {
    limit = pagination.value.rowsNumber;
  }
  const offset = (page - 1) * limit;
  requestRepeaters(limit, offset).then(() => {
    if (sortBy != null) {
      sortRepeaters(sortBy, descending);
    }
  });
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
