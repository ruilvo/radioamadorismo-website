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
      audio: {
        tip: 'Selecionar um som',
        icon: 'audio_file',
        label: 'Som',
        handler: selectAudio,
      },
      pdf: {
        tip: 'Selecionar um PDF',
        icon: 'picture_as_pdf',
        label: 'PDF',
        handler: selectPdf,
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
      ['image', 'audio', 'pdf'],
      ['viewsource'],
    ]"
  />
</template>

<script>
import { defineComponent, computed, ref } from "vue";

import { useQuasar } from "quasar";

import ImageSelectorDialog from "./rich_text_editor/ImageSelectorDialog.vue";
import AudioSelectorDialog from "./rich_text_editor/AudioSelectorDialog.vue";
import PdfSelectorDialog from "./rich_text_editor/PdfSelectorDialog.vue";

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
          if (!payload.imageHtml) {
            return;
          }
          editorRef.value.runCmd("insertHTML", payload.imageHtml);
        });
      },
      selectAudio() {
        $q.dialog({
          component: AudioSelectorDialog,
        }).onOk((payload) => {
          if (!payload.audioHtml) {
            return;
          }
          editorRef.value.runCmd("insertHTML", payload.audioHtml);
        });
      },
      selectPdf() {
        $q.dialog({
          component: PdfSelectorDialog,
        }).onOk((payload) => {
          if (!payload.pdfHtml) {
            return;
          }
          editorRef.value.runCmd("insertHTML", payload.pdfHtml);
        });
      },
    };
  },
});
</script>
