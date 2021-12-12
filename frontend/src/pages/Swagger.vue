<template>
  <div id="swagger-ui"></div>
</template>

<script>
import "swagger-ui/dist/swagger-ui.css";
import SwaggerUI from "swagger-ui";

export default {
  name: "Swagger",
  mounted() {
    SwaggerUI({
      url: "/openapi/",
      dom_id: "#swagger-ui",
    });
  },
};
</script>
