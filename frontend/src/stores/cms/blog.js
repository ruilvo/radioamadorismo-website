import { defineStore } from "pinia";

import { api } from "boot/axios";

export const useCmsBlogStore = defineStore("cms-blog", {
  state: () => ({
    posts: [],
  }),
  actions: {
    updatePosts() {
      api
        .get("/api/v1/cms/fact-blog-post/", { params: this.query })
        .then((res) => {
          this.posts = res.data;
        })
        .catch((err) => {
          console.error(err);
        });
    },
  },
});

export default useCmsBlogStore;
