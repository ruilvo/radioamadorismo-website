<template>
  <div id="map"></div>
</template>

<style lang="scss" scoped>
#map {
  max-width: 600px;
  height: 400px;
  margin: auto;
}
</style>

<script>
import * as L from "leaflet";

export default {
  name: "Map",
  props: {
    repeaters: Array,
  },

  mounted() {
    var mymap = L.map("map").setView([40, -8.0], 6);

    L.tileLayer(
      "https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token=pk.eyJ1IjoibWFwYm94IiwiYSI6ImNpejY4NXVycTA2emYycXBndHRqcmZ3N3gifQ.rJcFIG214AriISLbB6B5aw",
      {
        maxZoom: 18,
        attribution:
          'Map data &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, ' +
          'Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
        id: "mapbox/streets-v11",
        tileSize: 512,
        zoomOffset: -1,
      }
    ).addTo(mymap);
  },
};
</script>
