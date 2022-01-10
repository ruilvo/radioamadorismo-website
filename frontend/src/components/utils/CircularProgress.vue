<template>
  <q-circular-progress
    indeterminate
    size="50px"
    :thickness="0.22"
    color="lime"
    track-color="grey-3"
    class="q-ma-md"
  />
</template>

<script>
import { defineComponent } from "vue";

export default defineComponent({
  name: "CircularProgress",
});
</script>
