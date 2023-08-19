import { defineStore } from 'pinia';

export const useLeftDrawerStore = defineStore('left-drawer', {
  state: () => ({
    open: true,
  }),
  actions: {
    toggle() {
      this.open = !this.open;
    },
  },
  persist: true,
});
