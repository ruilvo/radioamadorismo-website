import { defineStore } from "pinia";

import { api } from "boot/axios";

export const useAuthStore = defineStore("auth", {
  state: () => ({
    username: null,
    token: null,
  }),
  actions: {
    async login({ username, password }) {
      try {
        var response = await api.post("/api/auth/dj-rest-auth/login/", {
          username,
          password,
        });
        this.username = username;
        this.token = response.data.key;
      } catch (error) {
        console.log(error);
      }
    },
    async logout() {
      try {
        await api.post("/api/auth/dj-rest-auth/logout/");
        this.username = null;
        this.token = null;
      } catch (error) {
        console.log(error);
      }
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
