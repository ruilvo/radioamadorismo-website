<template>
  <div class="overflow-auto">
    <h4>Editando as notas do repetidor {{ id }}: {{ callsign }}</h4>
    <div class="q-mt-md overflow-auto">
      <q-form class="q-gutter-sm" @submit="onSubmit">
        <div>
          <q-item-label>Notas</q-item-label>
          <RichTextEditor v-model="notes" />
        </div>

        <div>
          <q-btn label="Enviar" type="submit" color="primary" />
        </div>
      </q-form>
    </div>
  </div>
</template>

<script>
import { defineComponent, ref } from "vue";

import { useRouter } from "vue-router";

import { api } from "boot/axios";

import useRepeatersStore from "src/stores/repeaters";

import RichTextEditor from "components/utils/RichTextEditor";

export default defineComponent({
  name: "NotesEdit",
  components: {
    RichTextEditor,
  },
  props: {
    id: {
      type: String,
      required: true,
    },
  },
  setup(props) {
    const $router = useRouter();

    const repeatersStore = useRepeatersStore();

    const callsign = ref("");
    const notes = ref("");

    repeatersStore.getRepeater(props.id).then((response) => {
      notes.value = response.data.notes;
      callsign.value = response.data.callsign;
    });

    const onSubmit = () => {
      api
        .patch(`/api/v1/repeaters/fact-repeater/${props.id}/`, {
          notes: notes.value,
        })
        .then(() => {
          $router.push({ name: "repeaters-tree" });
        });
    };

    return {
      onSubmit,
      callsign,
      notes,
    };
  },
});
</script>
