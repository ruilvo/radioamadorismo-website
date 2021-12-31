<template>
  <q-select v-model="selectedImage" :options="imageOptions" label="Imagem" />

  <div class="row justify-center">
    <img
      v-if="selectedImageSource"
      :src="selectedImageSource"
      class="q-mt-md"
      width="400"
    />
  </div>

  <q-card-actions align="right" class="text-primary">
    <q-btn v-close-popup flat icon="close" label="Fechar" />
  </q-card-actions>
</template>

<script>
import { defineComponent, ref, computed, watch } from "vue";

import useImagestore from "src/stores/images";

export default defineComponent({
  name: "ImagesSelectorDialog",
  props: {
    modelValue: {
      type: String,
      required: false,
      default: null,
    },
  },
  emits: ["update:modelValue"],
  setup(props, { emit }) {
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

    watch(selectedImageSource, (val) => {
      if (val) {
        emit("update:modelValue", val);
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
    };
  },
});
</script>
