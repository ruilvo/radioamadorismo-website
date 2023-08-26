<template>
  <div class="q-pa-md">
    <div class="q-gutter-md">
      <h2>Diretório de Associações</h2>
      <q-separator />
      <div class="q-pa-md">
        <div class="row q-gutter-md">
          <q-card
            v-for="(association, i) in associations"
            :key="i"
            class="col-12 col-md-3"
          >
            <q-card-section>
              <div class="text-h6">
                {{ association.abrv }}: {{ association.name }}
              </div>
            </q-card-section>

            <q-separator inset />

            <q-card-section class="q-pt-none">
              <div class="column">
                <div v-if="association.email != ''">
                  e-email:
                  <a :href="'mailto:' + association.email">{{
                    association.email
                  }}</a>
                </div>
                <div v-if="association.website != ''">
                  website:
                  <a :href="association.website">{{ association.website }}</a>
                </div>
              </div>
            </q-card-section>
          </q-card>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, Ref } from 'vue';
import { api } from 'boot/axios';

import { Association } from 'src/components/models';

const associations: Ref<Array<Association>> = ref([]);

onMounted(async () => {
  try {
    const response = await api.get(
      '/api/v1/associations/association/?limit=100',
    );
    associations.value = response.data.results;
  } catch (error) {
    console.error(error);
  }
});
</script>
