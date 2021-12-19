<template>
  <div class="text-h6 q-mx-sm">Mapa de repetidores</div>
  <div
    class="col q-ml-md q-my-sm q-mr-sm"
    id="map"
    style="min-height: 200px"
  ></div>
</template>

<script>
import { defineComponent, onMounted, ref, watch } from "vue";

import "leaflet/dist/leaflet.css";
import * as L from "leaflet";

import { useRepeatersStore } from "src/stores/repeaters";

export default defineComponent({
  name: "RepeatersMap",
  setup() {
    const repeatersStore = useRepeatersStore();

    const repeatersMap = ref(null);
    const repeaterMarkers = ref([]);

    function updateMap() {
      if (!repeatersMap.value) return;
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
        var marker = L.marker([
          repeater.info_location.latitude,
          repeater.info_location.longitude,
        ]);

        // var circle = L.circle([51.508, -0.11], {
        //   color: 'red',
        //   fillColor: '#f03',
        //   fillOpacity: 0.5,
        //   radius: 500
        // }).addTo(map).bindPopup('I am a circle.');
        marker.addTo(repeatersMap.value);
        repeaterMarkers.value.push(marker);
      });
    }

    watch(repeatersStore, (new_store, old_store) => {
      updateMap();
    });

    onMounted(() => {
      repeatersMap.value = L.map("map").setView([40, -8.0], 6);

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
      ).addTo(repeatersMap.value);

      updateMap();
    });
  },
});
</script>
