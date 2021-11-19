<template>
  <div class="container" style="max-width: 1000px">
    <h2>Base de dados dos repetidores</h2>

    <table class="table thead-light table-striped">
      <thead class="table-dark">
        <tr>
          <th>Indicativo</th>
          <th>Região</th>
          <th>Local</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="item in repeaters" :key="item.callsign">
          <th>{{ item.callsign }}</th>
          <th>{{ item.info_location.region }}</th>
          <th>{{ item.info_location.place }}</th>
        </tr>
      </tbody>
    </table>
    <div id="map"></div>
  </div>
</template>

<style lang="scss" scoped>
#map {
  max-width: 600px;
  height: 400px;
  margin: auto;
}
</style>

<script>
import axios from "axios";
import * as L from "leaflet";

export default {
  name: "Repeaters",
  data() {
    return {
      repeaters: [],
    };
  },

  mounted() {
    this.getRepeaters();
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

  methods: {
    getRepeaters() {
      axios
        .get("/api/v1/")
        .then((res) => {
          this.repeaters = res.data;
        })
        .catch((err) => {
          console.log(err);
        });
    },
  },
};
</script>
