<template>
  <h2 class="text-center">Base de dados dos repetidores</h2>

  <div class="container-fluid" style="max-width: 1920px">
    <div class="row">
      <div class="col-sm-3">
        <Filters />
      </div>
      <div class="col-sm-9">
        <Table :repeaters="repeaters" />
        <Map :repeaters="repeaters" />
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import Map from "../components/repeaters/Map.vue";
import Table from "../components/repeaters/Table.vue";
import Filters from "../components/repeaters/Filters.vue";

export default {
  name: "Repeaters",
  data() {
    return {
      repeaters: [],
    };
  },

  components: {
    Map,
    Table,
    Filters,
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
