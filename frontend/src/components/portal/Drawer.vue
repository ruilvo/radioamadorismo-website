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
      <q-separator key="home-from-items" />
      <RepeatersItem />
      <q-separator key="items-from-meta" />
      <ApiItem />
      <AboutItem />
      <q-separator key="meta-from-auth" />
      <AuthItem />
    </q-list>
  </q-drawer>
</template>

<script>
import { defineComponent, computed } from "vue";

import StartPageItem from "components/common/drawer/StartPageItem.vue";
import AuthItem from "components/common/drawer/AuthItem.vue";

import RepeatersItem from "./drawer/RepeatersItem.vue";
import ApiItem from "./drawer/ApiItem.vue";
import AboutItem from "./drawer/AboutItem.vue";

export default defineComponent({
  name: "Drawer",
  components: {
    StartPageItem,
    AuthItem,
    RepeatersItem,
    ApiItem,
    AboutItem,
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
