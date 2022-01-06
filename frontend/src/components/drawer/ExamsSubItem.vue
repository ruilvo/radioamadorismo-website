<template>
  <q-expansion-item
    key="exams-item"
    v-model="exams_expanded"
    expand-separator
    icon="quiz"
    :to="{ name: 'exams' }"
    label="Perguntas de exame"
  >
    <q-item
      key="exams-cat3-item"
      clickable
      :to="{ name: 'exams-category', params: { category: 3 } }"
      exact
      :inset-level="1"
    >
      <q-item-section avatar>3️⃣</q-item-section>
      <q-item-section>Categoria 3</q-item-section>
    </q-item>
    <q-item
      key="exams-cat2-item"
      clickable
      :to="{ name: 'exams-category', params: { category: 2 } }"
      exact
      :inset-level="1"
    >
      <q-item-section avatar>2️⃣</q-item-section>
      <q-item-section>Categoria 2</q-item-section>
    </q-item>
    <q-item
      key="exams-cat1-item"
      clickable
      :to="{ name: 'exams-category', params: { category: 1 } }"
      exact
      :inset-level="1"
    >
      <q-item-section avatar>1️⃣</q-item-section>
      <q-item-section>Categoria 1</q-item-section>
    </q-item>
  </q-expansion-item>
</template>

<script>
import { defineComponent, ref, watch } from "vue";

import { useRoute } from "vue-router";

export default defineComponent({
  name: "ExamsItem",
  setup() {
    const $route = useRoute();

    const exams_expanded = ref($route.path.includes("/exames"));

    watch($route, (to) => {
      if (to.path.includes("/exames")) {
        exams_expanded.value = true;
      }
    });

    return {
      exams_expanded,
    };
  },
});
</script>
