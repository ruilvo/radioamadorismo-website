<template>
  <div class="row">
    <div class="col-12" style="height: 400px">
      <DynamicMap :initial-zoom="initialZoom" :initial-center="initialCenter">
        <l-marker-cluster-group :chunked-loading="true">
          <l-marker
            v-for="item in mapData"
            :key="item.id"
            :lat-lng="item.latLng"
          >
            <l-popup>
              <router-link
                :to="{ name: 'repeater_detail', params: { id: item.id } }"
              >
                <h4>{{ item.callsign }}</h4>
              </router-link>
            </l-popup>
          </l-marker>
        </l-marker-cluster-group>
      </DynamicMap>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';

import { components } from 'src/types/api';

import L from 'leaflet';
globalThis.L = L;

import 'vue-leaflet-markercluster/dist/style.css';

import { LMarker, LPopup } from '@vue-leaflet/vue-leaflet';
import { LMarkerClusterGroup } from 'vue-leaflet-markercluster';

import DynamicMap from 'components/map/DynamicMap.vue';

type FactRepeater = components['schemas']['FactRepeater'];

const props = defineProps({
  repeaters: {
    type: Array as () => FactRepeater[],
    required: true,
  },
});

const initialZoom = 6;
const initialCenter = [39.5, -17];

const mapData = computed(() => {
  return props.repeaters.map((repeater) => {
    return {
      id: repeater.id,
      callsign: repeater.callsign,
      latLng: [
        Number.parseFloat(repeater.info_location?.latitude || '0'),
        Number.parseFloat(repeater.info_location?.longitude || '0'),
      ],
    };
  });
});
</script>
