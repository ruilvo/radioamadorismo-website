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
    getPost(id) {
      return api.get(`/api/v1/cms/fact-blog-post/${id}/`);
    },
    deletePost(id) {
      return api.delete(`/api/v1/cms/fact-blog-post/${id}/`);
    },
    updatePost(id, newPost) {
      return api.patch(`/api/v1/cms/fact-blog-post/${id}/`, newPost);
    },
    createPost(newPost) {
      return api.post("/api/v1/cms/fact-blog-post/", newPost);
    },
  },
});

export default useCmsBlogStore;
