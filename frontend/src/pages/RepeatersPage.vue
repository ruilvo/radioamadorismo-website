<template>
  <div class="q-pa-md">
    <div class="q-gutter-md">
      <h2>Repetidores</h2>
      <q-separator />
      <q-banner inline-actions class="text-white bg-red">
        <h5><b>Página em construção.</b></h5>
        Mais detalhes podem ser consultados usando diretamente a API, usando as
        ligações na barra lateral.
      </q-banner>
      <q-separator />
      <h3>Listagem de repetidores</h3>
      <RepeatersTable />
      <q-separator />
      <RepeatersExport />
    </div>
  </div>
</template>

<script setup lang="ts">
import RepeatersTable from 'components/repeaters/RepeatersTable.vue';
import RepeatersExport from 'components/repeaters/RepeatersExport.vue';
</script>
