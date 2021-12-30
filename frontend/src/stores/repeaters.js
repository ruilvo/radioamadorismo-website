import { defineStore } from "pinia";

import { api } from "boot/axios";

export const useRepeatersStore = defineStore("repeaters", {
  state: () => ({
    count: 0,
    repeaters: [],
    query: {},
  }),
  actions: {
    async updateRepeaters(offset = 0, limit = 100, append = false) {
      const query = { offset, limit, ...this.query };
      const res = await api.get("/api/v1/repeaters/fact-repeater/", {
        params: query,
      });
      if (!append) {
        this.repeaters = res.data.results;
      } else {
        this.repeaters = [...this.repeaters, ...res.data.results];
      }
      this.count = res.data.count;
    },
  },
});

export default useRepeatersStore;
