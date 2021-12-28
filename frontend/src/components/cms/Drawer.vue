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
      <BlogItem />
      <q-separator key="items-from-auth" />
      <AuthItem />
    </q-list>
  </q-drawer>
</template>

<script>
import { defineComponent, computed } from "vue";

import StartPageItem from "components/common/drawer/StartPageItem.vue";
import AuthItem from "components/common/drawer/AuthItem.vue";
import BlogItem from "components/cms/drawer/BlogItem.vue";

export default defineComponent({
  name: "Drawer",
  components: {
    StartPageItem,
    AuthItem,
    BlogItem,
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
