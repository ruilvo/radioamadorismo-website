<template>
  <q-layout view="hhh lpr fff">
    <Header no-hamburger />

    <q-page-container>
      <router-view />
    </q-page-container>
  </q-layout>
</template>

<script>
import { defineComponent } from "vue";

import Header from "components/common/Header.vue";

export default defineComponent({
  name: "EmptyLayout",
  components: {
    Header,
  },
});
</script>
