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
    deletePdf(id) {
      return api.delete(`/api/v1/cms/fact-pdf/${id}/`);
    },
    updatePdf(id, newPdf) {
      return api.patch(`/api/v1/cms/fact-pdf/${id}/`, newPdf);
    },
    createPdf(newPdf) {
      return api.post("/api/v1/cms/fact-pdf/", newPdf);
    },
  },
});

export default usePdfStore;
