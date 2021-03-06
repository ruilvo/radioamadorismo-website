<template>
  <div class="column full-height">
    <div class="col-auto text-h6">Mapa de repetidores</div>
    <div class="col">
      <div id="map" style="min-height: 300px; height: 100%"></div>
    </div>
  </div>
</template>

<script>
import { defineComponent, onMounted, ref, watch } from "vue";

import "leaflet/dist/leaflet.css";

// https://stackoverflow.com/a/55525743/5168563
import iconRetinaUrl from "leaflet/dist/images/marker-icon-2x.png";
import iconUrl from "leaflet/dist/images/marker-icon.png";
import shadowUrl from "leaflet/dist/images/marker-shadow.png";

import * as L from "leaflet";

delete L.Icon.Default.prototype._getIconUrl;

L.Icon.Default.imagePath = ".";
L.Icon.Default.mergeOptions({
  iconRetinaUrl: iconRetinaUrl,
  iconUrl: iconUrl,
  shadowUrl: shadowUrl,
});

let repeatersMap = null;

import useRepeatersStore from "src/stores/repeaters";

export default defineComponent({
  name: "RepeatersMap",
  setup() {
    const repeatersStore = useRepeatersStore();

    const repeaterMarkers = ref([]);

    function updateMap() {
      if (!repeatersMap) return;
      repeaterMarkers.value.forEach((marker) => {
        marker.remove();
      });
      repeaterMarkers.value = [];
      repeatersStore.repeaters.forEach((repeater) => {
        if (!repeater.info_location) return;
        if (
          !(repeater.info_location.latitude && repeater.info_location.longitude)
        )
          return;
        let marker = L.marker([
          repeater.info_location.latitude,
          repeater.info_location.longitude,
        ]);

        marker.addTo(repeatersMap);
        marker.bindPopup(repeater.callsign);
        repeaterMarkers.value.push(marker);
      });
    }

    watch(repeatersStore, () => {
      updateMap();
    });

    onMounted(() => {
      repeatersMap = L.map("map").setView([40, -8.0], 6);

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
      ).addTo(repeatersMap);

      updateMap();
    });
  },
});
</script>
