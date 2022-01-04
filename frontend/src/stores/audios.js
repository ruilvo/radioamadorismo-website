import { defineStore } from "pinia";

import { api } from "boot/axios";

export const useAudioStore = defineStore("audios", {
  state: () => ({
    count: 0,
    audios: [],
  }),
  actions: {
    async updateAudios(offset = 0, limit = 100, append = false) {
      const res = await api.get("/api/v1/cms/fact-audio/", {
        params: {
          offset: offset,
          limit: limit,
        },
      });
      if (!append) {
        this.audios = res.data.results;
      } else {
        this.audios = [...this.audios, ...res.data.results];
      }
      this.count = res.data.count;
    },
    getAudio(id) {
      return api.get(`/api/v1/cms/fact-audio/${id}/`);
    },
    deleteAudio(id) {
      return api.delete(`/api/v1/cms/fact-audio/${id}/`);
    },
    updateAudio(id, newAudio) {
      return api.patch(`/api/v1/cms/fact-audio/${id}/`, newAudio);
    },
    createPdf(newAudio) {
      return api.post("/api/v1/cms/fact-audio/", newAudio);
    },
  },
});

export default useAudioStore;
