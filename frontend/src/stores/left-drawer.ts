import { defineStore } from 'pinia';

interface LeftDrawerState {
  open: boolean;
}

export const useLeftDrawerStore = defineStore('left-drawer', {
  state: (): LeftDrawerState => ({
    open: true,
  }),
  actions: {
    toggle() {
      this.open = !this.open;
    },
  },
  persist: true,
});
