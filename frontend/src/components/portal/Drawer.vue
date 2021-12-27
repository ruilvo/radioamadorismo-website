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
import RepeatersItem from "components/portal/drawer/RepeatersItem.vue";
import ApiItem from "components/portal/drawer/ApiItem.vue";
import AboutItem from "components/portal/drawer/AboutItem.vue";
import AuthItem from "components/portal/drawer/AuthItem.vue";

export default defineComponent({
  name: "Drawer",
  components: {
    StartPageItem,
    RepeatersItem,
    ApiItem,
    AboutItem,
    AuthItem,
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
