import { defineStore } from "pinia";

import { api } from "boot/axios";

export const useImageStore = defineStore("images", {
  state: () => ({
    count: 0,
    images: [],
  }),
  actions: {
    async updateImages(offset = 0, limit = 100, append = false) {
      const res = await api.get("/api/v1/cms/fact-image/", {
        params: {
          offset: offset,
          limit: limit,
        },
      });
      if (!append) {
        this.images = res.data.results;
      } else {
        this.images = [...this.images, ...res.data.results];
      }
      this.count = res.data.count;
    },
    getImage(id) {
      return api.get(`/api/v1/cms/fact-image/${id}/`);
    },
    deleteImage(id) {
      return api.delete(`/api/v1/cms/fact-image/${id}/`);
    },
    updateImage(id, newImage) {
      return api.patch(`/api/v1/cms/fact-image/${id}/`, newImage);
    },
    createImage(newImage) {
      return api.post("/api/v1/cms/fact-image/", newImage);
    },
  },
});

export default useImageStore;
