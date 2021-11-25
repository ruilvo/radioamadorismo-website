<template>
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
</template>

<script>
import { state } from "../../shared/repeaters.js";

export default {
  name: "Table",

  data() {
    return {
      repeaters: state.repeaters,
    };
  },
};
</script>
