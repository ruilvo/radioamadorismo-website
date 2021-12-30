<template>
  <q-drawer
    v-model="leftDrawerOpen"
    show-if-above
    side="left"
    bordered
    class="bg-grey-3"
  >
    <q-list>
      <StartPageItem />
      <q-separator key="home-from-meta" />
      <ApiItem />
      <q-separator key="meta-from-auth" />
      <AuthItem />
    </q-list>
  </q-drawer>
</template>

<script>
import { defineComponent, computed } from "vue";

import StartPageItem from "./drawer/StartPageItem.vue";
import AuthItem from "./drawer/AuthItem.vue";
import ApiItem from "./drawer/ApiItem.vue";

export default defineComponent({
  name: "Drawer",
  components: {
    StartPageItem,
    AuthItem,
    ApiItem,
  },
  props: {
    modelValue: Boolean,
  },
  emits: ["update:modelValue"],
  setup(props, { emit }) {
    const leftDrawerOpen = computed({
      get: () => props.modelValue,
      set: (val) => {
        emit("update:modelValue", val);
      },
    });

    return {
      leftDrawerOpen,
    };
  },
});
</script>
