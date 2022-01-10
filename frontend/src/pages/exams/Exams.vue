<template>
  <div>
    <h2>Perguntas de exame</h2>
    <hr />
    <div v-if="!question_mode">
      <p>Aqui nesta secção está disponível um sistema de perguntas de exame.</p>
      <p>
        Escolha a categoria no menu de navegação. Uma pergunta ao acaso da
        categoria correspondente será selecionada.
      </p>
    </div>

    <div v-if="question_mode && !question_data">
      <q-circular-progress
        indeterminate
        size="50px"
        :thickness="0.22"
        color="lime"
        track-color="grey-3"
        class="q-ma-md"
      />
    </div>
    <div v-if="question_data">
      <div class="text-body1 q-mb-sm">{{ question_data.question }}</div>
      <img
        v-if="!!question_data.question_image"
        :src="question_data.question_image"
      />
      <q-list class="q-mb-sm">
        <q-item v-ripple tag="label">
          <q-item-section avatar>
            <q-radio v-model="answer" val="A" />
          </q-item-section>
          <q-item-section>
            <q-item-label>{{ question_data.answer_a }}</q-item-label>
          </q-item-section>
        </q-item>
        <q-item v-ripple tag="label">
          <q-item-section avatar>
            <q-radio v-model="answer" val="B" />
          </q-item-section>
          <q-item-section>
            <q-item-label>{{ question_data.answer_b }}</q-item-label>
          </q-item-section>
        </q-item>
        <q-item v-ripple tag="label">
          <q-item-section avatar>
            <q-radio v-model="answer" val="C" />
          </q-item-section>
          <q-item-section>
            <q-item-label>{{ question_data.answer_c }}</q-item-label>
          </q-item-section>
        </q-item>
        <q-item v-ripple tag="label">
          <q-item-section avatar>
            <q-radio v-model="answer" val="D" />
          </q-item-section>
          <q-item-section>
            <q-item-label>{{ question_data.answer_d }}</q-item-label>
          </q-item-section>
        </q-item>
      </q-list>
      <q-banner
        v-if="answer_correct"
        inline-actions
        class="text-white bg-positive q-mb-sm"
      >
        A resposta esta correta!
      </q-banner>
      <q-banner
        v-if="answer_incorrect"
        inline-actions
        class="text-white bg-negative q-mb-sm"
      >
        A resposta esta incorreta!
      </q-banner>
      <q-btn
        color="primary"
        label="Pergunta aleatória"
        @click="next_question"
      />
    </div>
  </div>
</template>

<script>
import { defineComponent, ref, watch } from "vue";

import { api } from "boot/axios";

import { useRouter } from "vue-router";

export default defineComponent({
  name: "Exams",
  props: {
    category: {
      type: String,
      required: false,
      default: null,
    },
    id: {
      type: String,
      required: false,
      default: null,
    },
  },
  setup(props) {
    const $router = useRouter();

    const question_mode = ref(false);

    const question_data = ref(null);
    const question_count = ref(0);

    const answer = ref(null);
    const answer_correct = ref(false);
    const answer_incorrect = ref(false);

    const resolve_question = () => {
      question_mode.value = false;
      // question_data.value = null;
      answer.value = null;
      answer_correct.value = false;
      answer_incorrect.value = false;
      if (props.category !== null) {
        question_mode.value = true;

        if (props.id !== null) {
          // Get the question
          api
            .get(`/api/v1/exams/fact-exam-question/${props.id}`)
            .then((response) => {
              question_data.value = response.data;
            });
        } else {
          // Discover how many questions are in this category
          api
            .get("/api/v1/exams/fact-exam-question/", {
              params: {
                offset: 0,
                limit: 1,
                category: props.category,
              },
            })
            .then((response) => {
              question_count.value = response.data.count;
              // Then get a random question
              api
                .get("/api/v1/exams/fact-exam-question/", {
                  params: {
                    offset: Math.floor(Math.random() * question_count.value),
                    limit: 1,
                    category: props.category,
                  },
                })
                .then((response) => {
                  question_data.value = response.data.results[0];
                  $router.push({
                    name: "exams-question",
                    params: {
                      category: props.category,
                      id: question_data.value.id,
                    },
                  });
                });
            });
        }
      }
    };

    resolve_question();

    watch(props, () => {
      resolve_question();
    });

    watch(answer, () => {
      if (answer.value === question_data.value.correct_answer) {
        answer_correct.value = true;
        answer_incorrect.value = false;
      } else {
        answer_incorrect.value = true;
        answer_correct.value = false;
      }
    });

    return {
      question_mode,
      question_data,
      answer,
      answer_correct,
      answer_incorrect,
      next_question() {
        $router.push({
          name: "exams-category",
          params: {
            category: props.category,
          },
        });
      },
    };
  },
});
</script>
