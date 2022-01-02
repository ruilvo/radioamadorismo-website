<template>
  <RepeatersSubItem />
  <q-item
    key="aprs-passcode-item"
    clickable
    :to="{ name: 'aprs-passcode' }"
    exact
  >
    <q-item-section avatar>
      <q-icon name="settings_input_antenna" />
    </q-item-section>
    <q-item-section>Passcodes APRS-IS</q-item-section>
  </q-item>
</template>

<script>
import { defineComponent } from "vue";

import RepeatersSubItem from "./RepeatersSubItem.vue";

export default defineComponent({
  name: "StartPageItem",
  components: {
    RepeatersSubItem,
  },
});
</script>
