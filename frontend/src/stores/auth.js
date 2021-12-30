import { defineStore } from "pinia";

import { api } from "boot/axios";

export const useAuthStore = defineStore("auth", {
  state: () => ({
    isAuthenticated: false,
    errorMessage: null,
  }),
  actions: {
    async login(username, password) {
      try {
        await api.post("/api/auth/dj-rest-auth/login/", { username, password });
        this.isAuthenticated = true;
        this.errorMessage = null;
      } catch (error) {
        this.isAuthenticated = false;
        this.errorMessage = error.response.data.non_field_errors[0];
      }
    },
    async logout() {
      try {
        await api.post("/api/auth/dj-rest-auth/logout/");
        this.errorMessage = null;
      } catch (error) {
        this.errorMessage = error.response.data.non_field_errors[0];
      }
      // "Logout" regardless
      this.isAuthenticated = false;
    },
    async check() {
      try {
        await api.get("/api/auth/dj-rest-auth/user/");
        this.isAuthenticated = true;
      } catch {
        this.isAuthenticated = false;
      }
      this.errorMessage = null; // Be silent about it
    },
  },
  persist: {
    enabled: true,
  },
});

export default useAuthStore;
