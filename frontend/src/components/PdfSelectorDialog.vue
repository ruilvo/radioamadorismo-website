<template>
  <q-dialog ref="dialogRef" full-width full-height @hide="onDialogHide">
    <q-card class="q-dialog-plugin">
      <q-card-section>
        <q-select v-model="selectedPdf" :options="pdfOptions" label="PDF" />
        <div class="row justify-center q-my-md">
          <q-input
            v-model="pdfWidth"
            type="text"
            class="col-auto"
            label="Largura"
          />
          <div class="col-auto q-mx-md" />
          <q-input
            v-model="pdfHeight"
            type="text"
            class="col-auto"
            label="Altura"
          />
        </div>
        <div class="row justify-center">
          <div class="col">
            <div align="center">
              <iframe
                v-if="selectedPdfSource"
                :src="selectedPdfSource"
                class="col q-mt-md"
                :width="pdfWidth"
                :height="pdfHeight"
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
import { defineComponent, ref, computed, watch } from "vue";

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
    const selectedPdfSource = ref(null);
    const pdfHeight = ref("300px");
    const pdfWidth = ref("100%");

    watch(selectedPdf, (val) => {
      if (val) {
        pdfStore.getPdf(val.value).then((result) => {
          selectedPdfSource.value = result.data.file;
        });
      }
    });

    const pdfOptions = computed(() => {
      return pdfStore.pdfs.map((pdf) => {
        return {
          label: pdf.title,
          value: pdf.id,
        };
      });
    });

    return {
      selectedPdf,
      pdfOptions,
      selectedPdfSource,
      dialogRef,
      pdfHeight,
      pdfWidth,
      onDialogHide,
      onCancelClick: onDialogCancel,
      onOKClick() {
        onDialogOK({
          selectedPdfSource: selectedPdfSource.value,
          pdfHeight: pdfHeight.value,
          pdfWidth: pdfWidth.value,
        });
      },
    };
  },
});
</script>
