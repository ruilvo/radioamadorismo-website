<template>
  <q-dialog ref="dialogRef" full-width full-height @hide="onDialogHide">
    <q-card class="q-dialog-plugin">
      <q-card-section>
        <q-select
          v-model="selectedImage"
          :options="imageOptions"
          label="Imagem"
        />
        <div class="row justify-center">
          <img
            v-if="selectedImageSource"
            :src="selectedImageSource"
            class="q-mt-md"
            width="400"
          />
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

import useImagestore from "src/stores/images";

export default defineComponent({
  name: "ImagesSelectorDialog",
  emits: [...useDialogPluginComponent.emits],
  setup() {
    const { dialogRef, onDialogHide, onDialogOK, onDialogCancel } =
      useDialogPluginComponent();

    const imageStore = useImagestore();

    // Obtain the count then obtain the whole lot
    imageStore.updateImages(0, 1).then(() => {
      imageStore.updateImages(0, imageStore.count);
    });

    const selectedImage = ref(null);
    const selectedImageSource = ref(null);

    watch(selectedImage, (val) => {
      if (val) {
        imageStore.getImage(val.value).then((result) => {
          selectedImageSource.value = result.data.file;
          console.log(selectedImageSource.value);
        });
      }
    });

    const imageOptions = computed(() => {
      return imageStore.images.map((image) => {
        return {
          label: image.title,
          value: image.id,
        };
      });
    });

    return {
      selectedImage,
      imageOptions,
      selectedImageSource,
      dialogRef,
      onDialogHide,
      onCancelClick: onDialogCancel,
      onOKClick() {
        onDialogOK({
          selectedImageSource: selectedImageSource.value,
        });
      },
    };
  },
});
</script>
