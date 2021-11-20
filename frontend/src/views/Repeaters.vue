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
    <Map />
  </div>
</template>

<script>
import axios from "axios";
import Map from "../components/Map.vue";

export default {
  name: "Repeaters",
  data() {
    return {
      repeaters: [],
    };
  },

  components: {
    Map,
  },

  mounted() {
    this.getRepeaters();
  },

  methods: {
    getRepeaters() {
      axios
        .get("/api/v1/repeaters/")
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
