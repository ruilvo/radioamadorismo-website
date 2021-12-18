<template>
  <q-page>
    <div class="row">
      <div
        class="col-xs-12 col-sm-6 col-md-3"
        style="width: 100%; max-width: 300px"
      >
        <RepeatersFilter />
      </div>
      <div class="col-xs-12 col-sm col-md"><router-view /></div>
    </div>
  </q-page>
</template>

<script>
import RepeatersFilter from "src/components/repeaters/RepeatersFilter";

export default {
  name: "Repeaters",
  components: {
    RepeatersFilter,
  },
};
</script>
