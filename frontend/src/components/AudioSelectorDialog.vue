<template>
  <q-dialog ref="dialogRef" full-width full-height @hide="onDialogHide">
    <q-card class="q-dialog-plugin">
      <q-card-section>
        <q-select
          v-model="selectedAudio"
          :options="audioOptions"
          label="Audio"
        />
        <div class="row justify-center q-my-md">
          <q-input
            v-model="audioWidth"
            type="text"
            class="col-auto"
            label="Largura"
          />
        </div>
        <div class="row justify-center">
          <div class="col">
            <div align="center">
              <audio
                v-if="selectedAudioSource"
                controls
                :src="selectedAudioSource"
                class="col q-mt-md"
                :style="{ width: audioWidth }"
              >
                Your browser does not support the <code>audio</code> element.
              </audio>
            </div>
          </div>
        </div>
      </q-card-section>

      <q-card-actions align="center">
        <q-btn
          color="red"
          icon="cancel"
          label="Cancelar"
          @click="onCancelClick"
        />
        <q-btn color="primary" icon="done" label="OK" @click="onOKClick" />
      </q-card-actions>
    </q-card>
  </q-dialog>
</template>

<script>
import { defineComponent, ref, computed, watch } from "vue";

import { useDialogPluginComponent } from "quasar";

import useAudioStore from "src/stores/audios";

export default defineComponent({
  name: "AudioSelectorDialog",
  emits: [...useDialogPluginComponent.emits],
  setup() {
    const { dialogRef, onDialogHide, onDialogOK, onDialogCancel } =
      useDialogPluginComponent();

    const audioStore = useAudioStore();

    // Obtain the count then obtain the whole lot
    audioStore.updateAudios(0, 1).then(() => {
      audioStore.updateAudios(0, audioStore.count);
    });

    const selectedAudio = ref(null);
    const selectedAudioSource = ref(null);
    const audioWidth = ref("50%");

    watch(selectedAudio, (val) => {
      if (val) {
        audioStore.getAudio(val.value).then((result) => {
          selectedAudioSource.value = result.data.file;
        });
      }
    });

    const audioOptions = computed(() => {
      return audioStore.audios.map((audio) => {
        return {
          label: audio.title,
          value: audio.id,
        };
      });
    });

    return {
      selectedAudio,
      audioOptions,
      selectedAudioSource,
      dialogRef,
      audioWidth,
      onDialogHide,
      onCancelClick: onDialogCancel,
      onOKClick() {
        onDialogOK({
          selectedAudioSource: selectedAudioSource.value,
          audioWidth: audioWidth.value,
        });
      },
    };
  },
});
</script>
