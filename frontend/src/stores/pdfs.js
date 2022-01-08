import { defineStore } from "pinia";

import { api } from "boot/axios";

export const usePdfStore = defineStore("pdfs", {
  state: () => ({
    count: 0,
    pdfs: [],
  }),
  actions: {
    async updatePdfs(offset = 0, limit = 100, append = false) {
      const res = await api.get("/api/v1/cms/fact-pdf/", {
        params: {
          offset: offset,
          limit: limit,
        },
      });
      if (!append) {
        this.pdfs = res.data.results;
      } else {
        this.pdfs = [...this.pdfs, ...res.data.results];
      }
      this.count = res.data.count;
    },
    getPdf(id) {
      return api.get(`/api/v1/cms/fact-pdf/${id}/`);
    },
  },
});

export default usePdfStore;
