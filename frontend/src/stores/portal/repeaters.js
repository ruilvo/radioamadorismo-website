import { defineStore } from "pinia";

import { api } from "boot/axios";

export const useRepeatersStore = defineStore("repeaters", {
  state: () => ({
    repeaters: [],
    query: {},
  }),
  actions: {
    async updateRepeaters() {
      const res = await api.get("/api/v1/repeaters/fact-repeater/", {
        params: this.query,
      });
      this.repeaters = res.data.results;
    },
  },
});

export default useRepeatersStore;
