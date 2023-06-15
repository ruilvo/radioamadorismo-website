<template>
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
  <!-- Other items here -->
</template>

<script lang="ts">
import { defineComponent } from 'vue';

export default defineComponent({
  name: 'PagesItem',
});
</script>
