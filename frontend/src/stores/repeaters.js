import { defineStore } from "pinia";

import { api } from "boot/axios";

export const useRepeatersStore = defineStore("repeaters", {
  state: () => ({
    repeaters: [],
    query: {},
  }),
  actions: {
    updateRepeaters() {
      api
        .get("/api/v1/repeaters/", { params: this.query })
        .then((res) => {
          this.repeaters = res.data;
        })
        .catch((err) => {
          console.log(err);
        });
    },
  },
});
