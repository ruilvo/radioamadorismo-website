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
  <div class="row">
    <div class="col-12" style="height: 400px">
      <l-map
        :use-global-leaflet="false"
        :zoom="zoom"
        :center="mapPoint"
        @update:zoom="onZoomUpdated"
        ref="map"
      >
        <DyamicTileLayer :zoom="zoom" />
        <l-marker :lat-lng="mapPoint"> </l-marker>
      </l-map>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue';

import 'leaflet/dist/leaflet.css';
import { LMap, LMarker } from '@vue-leaflet/vue-leaflet';

import { components } from 'src/types/api';

import DyamicTileLayer from 'components/map/DynamicTileLayer.vue';

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

const zoom = ref(15);

function onZoomUpdated(newZoom: number) {
  zoom.value = newZoom;
}

const mapPoint = computed(() => {
  if (props.info_location === null) {
    return [0, 0];
  }
  return [
    Number.parseFloat(props.info_location.latitude || '0'),
    Number.parseFloat(props.info_location.longitude || '0'),
  ];
});
</script>
