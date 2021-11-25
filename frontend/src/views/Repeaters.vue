<template>
  <h2 class="text-center">Base de dados dos repetidores</h2>

  <div class="container-fluid" style="max-width: 1920px">
    <div class="row">
      <div class="col-sm-3">
        <Filters />
      </div>
      <div class="col-sm-9">
        <ul class="nav nav-tabs">
          <li class="nav-item">
            <router-link
              class="nav-link"
              exact-active-class="active"
              to="/repetidores"
              >Tabela</router-link
            >
          </li>
          <li class="nav-item">
            <router-link
              class="nav-link"
              exact-active-class="active"
              to="/repetidores/mapa"
              >Mapa</router-link
            >
          </li>
        </ul>
        <router-view />
      </div>
    </div>
  </div>
</template>

<script>
import { ref } from "vue";
import axios from "axios";
import Filters from "../components/repeaters/Filters.vue";
import repeaters from "../shared/repeaters.js";

export default {
  name: "Repeaters",
  data() {
    return { repeaters };
  },

  components: {
    Filters,
  },

  mounted() {
    this.getRepeaters();
  },

  methods: {
    getRepeaters() {
      let data = ref([]);
      axios
        .get("/api/v1/repeaters/")
        .then((res) => {
          data.value = res.data;
        })
        .catch((err) => {
          console.log(err);
        })
        .then((data) => (self.repeaters = data));
    },
  },
};
</script>
