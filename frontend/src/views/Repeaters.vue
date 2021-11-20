<template>
  <h2 class="text-center">Base de dados dos repetidores</h2>

  <div class="container-fluid">
    <div class="row">
      <div class="col-sm-3">
        <div class="text-center">
          <h4>Filtros</h4>
        </div>
        Em construção...
      </div>
      <div class="col-sm-9">
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
    </div>
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
