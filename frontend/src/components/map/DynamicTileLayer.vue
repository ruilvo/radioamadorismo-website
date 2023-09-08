<template>
  <l-tile-layer
    :name="mapTileLayer.name"
    :url="mapTileLayer.url"
    :max-zoom="19"
    :attribution="mapTileLayer.attribution"
    layer-type="base"
  ></l-tile-layer>
</template>

<script setup lang="ts">
import { computed } from 'vue';

import { LTileLayer } from '@vue-leaflet/vue-leaflet';

const props = defineProps({
  zoom: {
    type: Number,
    required: true,
  },
});

type TileLayerParams = {
  name: string;
  url: string;
  maxZoom: number;
  attribution: string;
};

const valentimTileLayer = {
  name: 'Valentim',
  url: 'https://map.valentim.org/otmpt/{z}/{x}/{y}.png',
  maxZoom: 17,
  attribution:
    'Mosaico: <a href="http://valentim.org">valentim.org</a> | Dados: Contribuidores do <a href="http://www.openstreetmap.org/about">OpenStreetMap</a>, <a href="https://land.copernicus.eu/imagery-in-situ/eu-dem">Copernicus</a>, <a href="http://www.hidrografico.pt/op/33">Instituto Hidrográfico</a> | Estilo: <a href="https://github.com/der-stefan/OpenTopoMap">OpenTopoMap</a>, &copy; <a href="https://creativecommons.org/licenses/by-sa/3.0/">CC-BY-SA</a>',
};

const osmTileLayer: TileLayerParams = {
  name: 'OpenStreetMap',
  url: 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
  maxZoom: 19,
  attribution:
    '&copy; <a target="_blank" href="http://osm.org/copyright">OpenStreetMap</a> contributors',
};

const mapTileLayer = computed(() => {
  if (props.zoom < 9 || props.zoom > 17) {
    return osmTileLayer;
  }
  return valentimTileLayer;
});
</script>
