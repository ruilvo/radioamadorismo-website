<template>
  <Header />
  <div class="container-fluid">
    <router-view />
  </div>
</template>

<script>
import Header from "./components/Header.vue";

export default {
  name: "App",
  title: "Portal do radioamadorismo",
  components: {
    Header,
  },
};
</script>
