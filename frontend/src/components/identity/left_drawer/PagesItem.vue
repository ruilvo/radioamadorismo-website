<template>
  <q-item key="repeaters-item" clickable :to="{ name: 'repeaters' }" exact>
    <q-item-section avatar>
      <q-icon name="cell_tower" />
    </q-item-section>
    <q-item-section>Repetidores</q-item-section>
  </q-item>
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
