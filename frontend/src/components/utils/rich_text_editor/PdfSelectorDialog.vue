<template>
  <q-dialog ref="dialogRef" full-width full-height @hide="onDialogHide">
    <q-card class="q-dialog-plugin">
      <q-card-section>
        <q-select
          v-model="selectedPdf"
          :options="pdfOptions"
          emit-value
          map-options
          label="PDF"
        />
        <div class="row justify-center q-my-md">
          <q-input
            v-model="pdfWidth"
            type="text"
            class="col-auto q-mr-md"
            label="Largura (HTML)"
          />
          <q-input
            v-model="pdfHeight"
            type="text"
            class="col-auto"
            label="Altura (HTML)"
          />
        </div>
        <div class="row justify-center">
          <div class="col">
            <div align="center">
              <iframe
                v-if="selectedPdfSource"
                :src="selectedPdfSource"
                class="col q-mt-md"
                :style="{ width: pdfWidth, height: pdfHeight }"
                type="application/pdf"
              />
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
import { defineComponent, computed, ref } from "vue";

import { useDialogPluginComponent } from "quasar";

import usePdfStore from "src/stores/pdfs";

export default defineComponent({
  name: "PdfSelectorDialog",
  emits: [...useDialogPluginComponent.emits],
  setup() {
    const { dialogRef, onDialogHide, onDialogOK, onDialogCancel } =
      useDialogPluginComponent();

    const pdfStore = usePdfStore();
    // Obtain the count then obtain the whole lot
    pdfStore.updatePdfs(0, 1).then(() => {
      pdfStore.updatePdfs(0, pdfStore.count);
    });

    const selectedPdf = ref(null);
    const pdfOptions = computed(() => {
      return pdfStore.pdfs.map((pdf) => {
        return {
          label: pdf.title,
          value: pdf.id,
        };
      });
    });

    const selectedPdfSource = computed(() => {
      const elem = pdfStore.pdfs.find((pdf) => pdf.id === selectedPdf.value);
      return elem ? elem.file : null;
    });
    const pdfWidth = ref("80%");
    const pdfHeight = ref("400px");

    return {
      selectedPdf,
      pdfOptions,
      selectedPdfSource,
      pdfWidth,
      pdfHeight,
      // Dialog
      dialogRef,
      onDialogHide,
      onCancelClick: onDialogCancel,
      onOKClick() {
        onDialogOK({
          pdfHtml: `<div><iframe src="${selectedPdfSource.value}" style="width: ${pdfWidth.value}; height:${pdfHeight.value}" type="application/pdf" /></div>`,
        });
      },
    };
  },
});
</script>
