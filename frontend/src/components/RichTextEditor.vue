<template>
  <q-editor
    ref="editorRef"
    v-model="editorContent"
    min-height="5rem"
    :dense="$q.screen.lt.md"
    :definitions="{
      image: {
        tip: 'Selecionar uma imagem',
        icon: 'image',
        label: 'Imagem',
        handler: selectImage,
      },
    }"
    :toolbar="[
      [
        {
          label: $q.lang.editor.align,
          icon: $q.iconSet.editor.align,
          fixedLabel: true,
          options: ['left', 'center', 'right', 'justify'],
        },
      ],
      ['bold', 'italic', 'strike', 'underline', 'subscript', 'superscript'],
      ['token', 'hr', 'link', 'custom_btn'],
      [
        {
          label: $q.lang.editor.formatting,
          icon: $q.iconSet.editor.formatting,
          list: 'no-icons',
          options: ['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'code'],
        },
        {
          label: $q.lang.editor.fontSize,
          icon: $q.iconSet.editor.fontSize,
          fixedLabel: true,
          fixedIcon: true,
          list: 'no-icons',
          options: [
            'size-1',
            'size-2',
            'size-3',
            'size-4',
            'size-5',
            'size-6',
            'size-7',
          ],
        },
        'removeFormat',
      ],
      ['quote', 'unordered', 'ordered', 'outdent', 'indent'],
      ['undo', 'redo'],
      ['image'],
      ['viewsource'],
    ]"
  />
</template>

<script>
import { defineComponent, computed, ref } from "vue";

import { useQuasar } from "quasar";

import ImageSelectorDialog from "components/ImagesSelectorDialog";

export default defineComponent({
  name: "RichTextEditor",
  props: {
    modelValue: {
      type: String,
      required: true,
    },
  },
  emits: ["update:modelValue"],
  setup(props, { emit }) {
    const $q = useQuasar();

    const editorRef = ref(null);

    const editorContent = computed({
      get: () => props.modelValue,
      set: (val) => {
        emit("update:modelValue", val);
      },
    });

    return {
      editorRef,
      editorContent,
      selectImage() {
        $q.dialog({
          component: ImageSelectorDialog,
        }).onOk((payload) => {
          if (!payload.selectedImageSource) {
            return;
          }
          console.log("OK");
          console.log(payload);
          editorRef.value.runCmd(
            "insertHTML",
            `<img src="${payload.selectedImageSource}" />`
          );
        });
      },
    };
  },
});
</script>
