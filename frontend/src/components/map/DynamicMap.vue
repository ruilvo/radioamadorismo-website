<template>
  <l-map
    :zoom="zoom"
    :center="props.initialCenter as PointExpression"
    @update:zoom="onZoomUpdated"
    ref="map"
  >
    <DyamicTileLayer :zoom="zoom" />
    <slot> </slot>
  </l-map>
</template>

<script setup lang="ts">
import { ref, PropType } from 'vue';

import { LatLngExpression, PointExpression } from 'leaflet';
import { LMap } from '@vue-leaflet/vue-leaflet';

import DyamicTileLayer from 'components/map/DynamicTileLayer.vue';

const props = defineProps({
  initialZoom: {
    type: Number,
    required: true,
  },
  initialCenter: {
    type: Object as PropType<LatLngExpression>,
    required: true,
  },
});

const zoom = ref(props.initialZoom);

function onZoomUpdated(newZoom: number) {
  zoom.value = newZoom;
}
</script>
