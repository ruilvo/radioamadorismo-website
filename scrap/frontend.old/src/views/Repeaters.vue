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
              :to="{ path: '/repetidores', query: state.query }"
              >Tabela</router-link
            >
          </li>
          <li class="nav-item">
            <router-link
              class="nav-link"
              exact-active-class="active"
              :to="{ path: '/repetidores/mapa', query: state.query }"
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
import state from "../shared/repeaters.js";
import Filters from "../components/repeaters/Filters.vue";

export default {
  name: "Repeaters",
  data() {
    return {
      state,
    };
  },

  components: {
    Filters,
  },
};
</script>
