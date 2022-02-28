<template>
  <q-expansion-item key="api-tab" expand-separator icon="api" label="API">
    <q-item
      key="swagger-api"
      clickable
      tag="a"
      href="/api/reference/swagger-ui/"
      exact
      :inset-level="1"
    >
      <q-item-section avatar>
        <q-icon name="description" />
      </q-item-section>
      <q-item-section>Doc. (Swagger-UI) (🇬🇧)</q-item-section>
      <q-item-section side><q-icon name="launch" size="xs" /></q-item-section>
    </q-item>
    <q-item
      key="redoc"
      clickable
      tag="a"
      href="/api/reference/redoc/"
      exact
      :inset-level="1"
    >
      <q-item-section avatar>
        <q-icon name="description" />
      </q-item-section>
      <q-item-section>Doc. (Redoc) (🇬🇧)</q-item-section>
      <q-item-section side><q-icon name="launch" size="xs" /></q-item-section>
    </q-item>
    <q-item
      key="repeaters-api"
      clickable
      tag="a"
      href="/api/v1/repeaters/fact-repeater/"
      exact
      :inset-level="1"
    >
      <q-item-section avatar>
        <q-icon name="cell_tower" />
      </q-item-section>
      <q-item-section>Repetidores (🇬🇧)</q-item-section>
      <q-item-section side><q-icon name="launch" size="xs" /></q-item-section>
    </q-item>
  </q-expansion-item>
</template>

<script>
import { defineComponent } from "vue";

export default defineComponent({
  name: "ApiItem",
});
</script>
