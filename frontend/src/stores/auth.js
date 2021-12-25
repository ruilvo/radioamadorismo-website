import { defineStore } from "pinia";

import { api } from "boot/axios";

export const useAuthStore = defineStore("auth", {
  state: () => ({
    username: null,
    token: null,
  }),
  actions: {
    async login({ username, password }) {
      var response = await api.post("/api/auth/dj-rest-auth/login/", {
        username,
        password,
      });
      this.username = username;
      this.token = response.data.key;
    },
    async logout() {
      await api.post("/api/auth/dj-rest-auth/logout/");
      self.reset();
    },
    reset() {
      this.username = null;
      this.token = null;
    },
  },
  getters: {
    isLoggedIn: (state) => !!state.token,
  },
});
