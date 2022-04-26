<template>
  <q-header bordered class="bg-primary text-white">
    <q-toolbar>
      <q-btn
        v-if="!noHamburger"
        dense
        flat
        round
        icon="menu"
        @click="emitHamburgerClicked"
      />

      <q-toolbar-title class="row">
        <router-link to="/" style="text-decoration: none; color: inherit">
          <span class="text-italic q-mr-sm">Æ</span>
          <span class="q-mr-sm">Portal do Radioamador</span>
        </router-link>
      </q-toolbar-title>
    </q-toolbar>
  </q-header>
</template>

<script>
import { defineComponent } from "vue";

export default defineComponent({
  // eslint-disable-next-line vue/multi-word-component-names
  name: "Header",
  props: {
    noHamburger: Boolean,
  },
  emits: ["hamburgerClicked"],
  setup(props, { emit }) {
    return {
      emitHamburgerClicked() {
        emit("hamburgerClicked");
      },
    };
  },
});
</script>
