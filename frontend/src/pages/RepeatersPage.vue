<template>
  <div class="q-pa-md">
    <div class="q-gutter-md">
      <h2>Repetidores</h2>
      <q-separator />
      <q-banner inline-actions class="text-white bg-red">
        <h5><b>Página em construção.</b></h5>
        Por enquanto, a lista de repetidores pode ser consultada diretamente via
        API, usando a ligação na barra lateral.
      </q-banner>
      <div class="column q-px-md q-gutter-y-md">
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
    </div>
  </div>
</template>
