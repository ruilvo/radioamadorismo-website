<template>
  <div class="text-h6 q-mx-sm">Mapa de repetidores</div>
  <div
    class="col q-ml-md q-my-sm q-mr-sm"
    id="map"
    style="min-height: 200px"
  ></div>
</template>

<script>
import { defineComponent, onMounted } from "vue";

import "leaflet/dist/leaflet.css";

import * as L from "leaflet";

export default defineComponent({
  name: "RepeatersMap",
  setup() {
    onMounted(() => {
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
    });
  },
});
</script>
