<template>
  <MainLayout>
    <h3>Repetidores</h3>
    <hr />
    <q-banner inline-actions class="text-white bg-red">
      <h5><b>Página em construção.</b></h5>
      Por enquanto, a lista de repetidores pode ser consultada diretamente via
      API, usando a ligação na barra lateral.
    </q-banner>
    <div class="column q-pa-md q-gutter-y-md">
      <q-btn
        color="primary"
        label="Ficheiro CHIRP"
        href="/backend/repeaters/export/chirp/"
      />
      <q-btn
        color="primary"
        label="Ficheiro para Anytone D878UVII+"
        href="/backend/repeaters/export/d878uvii/codeplug/"
      />
    </div>
  </MainLayout>
</template>

<script setup lang="ts">
import MainLayout from 'components/layout/MainLayout.vue';
</script>
