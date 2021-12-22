<template>
  <div id="swagger-ui"></div>
</template>

<script>
import { defineComponent, onMounted } from "vue";

import "swagger-ui/dist/swagger-ui.css";
import SwaggerUI from "swagger-ui";

export default defineComponent({
  name: "Swagger",
  setup() {
    onMounted(() => {
      SwaggerUI({
        url: "/openapi/",
        dom_id: "#swagger-ui",
      });
    });
  },
});
</script>
