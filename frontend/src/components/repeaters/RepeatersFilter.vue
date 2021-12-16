<template>
  <div class="text-h6 q-ml-sm">Filtros</div>
  <div class="q-pa-md" style="max-width: 300px">
    <q-form @submit="onSubmit" @reset="onReset" class="q-gutter-md">
      <q-input
        filled
        v-model="name"
        label="Your name *"
        hint="Name and surname"
        lazy-rules
        :rules="[(val) => (val && val.length > 0) || 'Please type something']"
      />

      <q-input
        filled
        type="number"
        v-model="age"
        label="Your age *"
        lazy-rules
        :rules="[
          (val) => (val !== null && val !== '') || 'Please type your age',
          (val) => (val > 0 && val < 100) || 'Please type a real age',
        ]"
      />

      <q-toggle v-model="accept" label="I accept the license and terms" />

      <div>
        <q-btn label="Submit" type="submit" color="primary" />
        <q-btn
          label="Reset"
          type="reset"
          color="primary"
          flat
          class="q-ml-sm"
        />
      </div>
    </q-form>
  </div>
</template>

<script>
export default {
  name: "RepeatersFilter",
  data() {
    return {
      name: null,
      age: null,
      accept: false,
    };
  },
  methods: {
    onSubmit() {
      if (this.accept.value !== true) {
        console.log("You need to accept the license and terms first");
      } else {
        console.log("Submitted");
      }
    },
    onReset() {
      this.name = null;
      this.age = null;
      this.accept = false;
    },
  },
};
</script>
