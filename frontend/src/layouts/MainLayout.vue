<template>
  <q-layout view="hhh LpR fFf">
    <q-header bordered class="bg-primary text-white" height-hint="98">
      <q-toolbar>
        <q-toolbar-title shrink> Portal do Radioamadorismo </q-toolbar-title>
        <div class="lt-sm">
          <q-btn flat dense round icon="menu" />
        </div>
        <div>
          <q-btn class="sm:disabled" label="Repetidores" flat dense dense-lg />
        </div>
      </q-toolbar>
    </q-header>

    <q-page-container>
      <router-view />
    </q-page-container>
  </q-layout>
</template>

<script>
export default {
  name: "MainLayout",
};
</script>
