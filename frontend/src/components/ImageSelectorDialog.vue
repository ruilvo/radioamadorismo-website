<template>
  <q-dialog ref="dialogRef" full-width full-height @hide="onDialogHide">
    <q-card class="q-dialog-plugin">
      <q-card-section>
        <q-select
          v-model="selectedImage"
          :options="imageOptions"
          label="Imagem"
        />
        <div class="row justify-center q-my-md">
          <q-input
            v-model="imageWidth"
            type="number"
            class="col-auto"
            label="Largura"
          />
          <q-btn
            color="primary"
            :icon="keepAspectRatio ? 'lock' : 'lock_open'"
            class="col-auto q-mx-md"
            @click="keepAspectRatio = !keepAspectRatio"
          />
          <q-input
            v-model="imageHeight"
            type="number"
            class="col-auto"
            label="Altura"
          />
        </div>
        <div class="row justify-center">
          <img
            v-if="selectedImageSource"
            :src="selectedImageSource"
            class="q-mt-md"
            :width="imageWidth"
            :height="imageHeight"
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
    const selectedImageSource = ref(null);
    const imageHeight = ref(null);
    const imageWidth = ref(null);
    const aspectRatio = ref(null);
    const keepAspectRatio = ref(true);

    const avoidRecall = ref(false);
    watch([imageHeight, imageWidth], (newValues, oldValues) => {
      console.log(avoidRecall.value);
      if (avoidRecall.value) {
        avoidRecall.value = false;
        return;
      }
      avoidRecall.value = true;
      const oldHeight = oldValues[0];
      const oldWidth = oldValues[1];
      const newHeight = newValues[0];
      const newWidth = newValues[1];
      const heightChanged = oldHeight !== newHeight;
      const widthChanged = oldWidth !== newHeight;

      if (oldHeight && heightChanged && aspectRatio && keepAspectRatio.value) {
        imageWidth.value = Math.round(newHeight * aspectRatio.value);
      }

      if (oldWidth && widthChanged && aspectRatio && keepAspectRatio.value) {
        imageHeight.value = Math.round(newWidth / aspectRatio.value);
      }
    });

    watch(selectedImage, (val) => {
      if (val) {
        imageStore.getImage(val.value).then((result) => {
          avoidRecall.value = true;
          selectedImageSource.value = result.data.file;
          imageHeight.value = result.data.height;
          imageWidth.value = result.data.width;
          aspectRatio.value = imageWidth.value / imageHeight.value;
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
      imageHeight,
      imageWidth,
      keepAspectRatio,
      dialogRef,
      onDialogHide,
      onCancelClick: onDialogCancel,
      onOKClick() {
        onDialogOK({
          selectedImageSource: selectedImageSource.value,
          imageHeight: imageHeight.value,
          imageWidth: imageWidth.value,
        });
      },
    };
  },
});
</script>
