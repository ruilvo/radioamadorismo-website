import { defineStore } from "pinia";

import { api } from "boot/axios";

export const useBlogStore = defineStore("blog", {
  state: () => ({
    count: 0,
    posts: [],
  }),
  actions: {
    async updatePosts(offset = 0, limit = 100, append = false) {
      const res = await api.get("/api/v1/cms/fact-blog-post/", {
        params: {
          offset: offset,
          limit: limit,
        },
      });
      if (!append) {
        this.posts = res.data.results;
      } else {
        this.posts = [...this.posts, ...res.data.results];
      }
      this.count = res.data.count;
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

export default useBlogStore;
