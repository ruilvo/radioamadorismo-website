<template>
  <q-dialog ref="dialogRef" full-width full-height @hide="onDialogHide">
    <q-card class="q-dialog-plugin">
      <q-card-section>
        <q-select
          v-model="selectedImage"
          :options="imageOptions"
          emit-value
          map-options
          label="Imagem"
        />
        <div class="row justify-center q-my-md">
          <q-input
            v-model="imageWidth"
            type="text"
            class="col-auto"
            label="Largura (HTML)"
          />
        </div>
        <div class="row justify-center">
          <img
            :src="selectedImageSource"
            class="q-mt-md"
            :style="{ width: imageWidth }"
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
import { defineComponent, computed, ref } from "vue";

import { useDialogPluginComponent } from "quasar";

import useImageStore from "src/stores/images";

export default defineComponent({
  name: "ImageSelectorDialog",
  emits: [...useDialogPluginComponent.emits],
  setup() {
    const { dialogRef, onDialogHide, onDialogOK, onDialogCancel } =
      useDialogPluginComponent();

    const imageStore = useImageStore();
    // Obtain the count then obtain the whole lot
    imageStore.updateImages(0, 1).then(() => {
      imageStore.updateImages(0, imageStore.count);
    });

    const selectedImage = ref(null);
    const imageOptions = computed(() => {
      return imageStore.images.map((image) => {
        return {
          label: image.title,
          value: image.id,
        };
      });
    });

    const selectedImageSource = computed(() => {
      const elem = imageStore.images.find(
        (image) => image.id === selectedImage.value
      );
      return elem ? elem.file : null;
    });
    const imageWidth = ref("80%");

    return {
      selectedImage,
      imageOptions,
      selectedImageSource,
      imageWidth,
      // Dialog
      dialogRef,
      onDialogHide,
      onCancelClick: onDialogCancel,
      onOKClick() {
        onDialogOK({
          imageHtml: `<img src="${selectedImageSource.value}" style="width: ${imageWidth.value}">`,
        });
      },
    };
  },
});
</script>
