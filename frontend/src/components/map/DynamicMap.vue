<template>
  <l-map
    :zoom="zoom"
    :max-zoom="19"
    :center="props.initialCenter"
    @update:zoom="onZoomUpdated"
    ref="map"
  >
    <DyamicTileLayer :zoom="zoom" />
    <slot> </slot>
  </l-map>
</template>

<script setup lang="ts">
import { ref, PropType } from 'vue';

import 'leaflet/dist/leaflet.css';

import L from 'leaflet';
globalThis.L = L;

import { LMap } from '@vue-leaflet/vue-leaflet';

import DyamicTileLayer from 'components/map/DynamicTileLayer.vue';

const props = defineProps({
  initialZoom: {
    type: Number,
    required: true,
  },
  initialCenter: {
    type: Array as PropType<number[]>,
    required: true,
  },
});

const zoom = ref(props.initialZoom);

function onZoomUpdated(newZoom: number) {
  zoom.value = newZoom;
}
</script>
