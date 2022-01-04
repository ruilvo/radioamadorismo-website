<template>
  <div class="col column">
    <div class="text-h6 col-auto">Lista de repetidores</div>
    <div class="col">
      <q-input ref="filterRef" v-model="filter" filled label="Procurar">
        <template #append>
          <q-icon
            v-if="filter !== ''"
            name="clear"
            class="cursor-pointer"
            @click="resetFilter"
          />
        </template>
      </q-input>
      <q-tree
        :filter="filter"
        :filter-method="filterMethod"
        :nodes="repeatersAsQtree"
        node-key="id"
      >
        <template #header-repeater="prop">
          <div class="row items-center">
            <q-icon
              v-if="prop.node.icon"
              :name="prop.node.icon"
              color="orange"
              size="28px"
              class="q-mr-sm"
            />
            <div class="text-weight-bold text-primary">
              {{ prop.node.label }}
              <div class="q-gutter-xs">
                <q-badge v-if="prop.node.badge_on" color="positive" align="top"
                  >ON</q-badge
                >
                <q-badge v-if="prop.node.badge_off" color="negative" align="top"
                  >OFF</q-badge
                >
                <q-badge
                  v-if="prop.node.badge_project"
                  color="orange-8"
                  align="top"
                  >Projeto</q-badge
                >
                <q-badge
                  v-if="prop.node.badge_problems"
                  color="warning"
                  align="top"
                  >Problemas</q-badge
                >
                <q-badge
                  v-if="prop.node.badge_other"
                  color="warning"
                  align="top"
                  >Situação desconhecida</q-badge
                >
                <q-badge
                  v-if="prop.node.badge_half_duplex"
                  color="info"
                  align="top"
                  >Semi-duplex</q-badge
                >
                <q-badge
                  v-if="prop.node.badge_simplex"
                  color="warning"
                  align="top"
                  >Simplex</q-badge
                >
                <q-badge v-if="prop.node.badge_2m" color="brown-8" align="top"
                  >2m</q-badge
                >
                <q-badge
                  v-if="prop.node.badge_70cm"
                  color="deep-orange-6"
                  align="top"
                  >70cm</q-badge
                >
              </div>
              <div class="q-gutter-xs">
                <q-badge v-if="prop.node.badge_fm" color="secondary" align="top"
                  >FM</q-badge
                >
                <q-badge v-if="prop.node.badge_dstar" color="accent" align="top"
                  >D-STAR</q-badge
                >
                <q-badge
                  v-if="prop.node.badge_fusion"
                  color="negative"
                  align="top"
                  >Fusion/C4FM</q-badge
                >
                <q-badge v-if="prop.node.badge_dmr" color="positive" align="top"
                  >DMR</q-badge
                >
              </div>
            </div>
          </div>
        </template>

        <template #body-repeater="prop">
          <div class="row">
            <div class="full-width q-mb-sm">
              <q-btn
                v-if="authStore.isAuthenticated"
                icon="edit"
                color="primary"
                @click="
                  $router.push({
                    name: 'repeater-notes-edit',
                    params: { id: prop.node.repeater_id },
                  })
                "
                >Editar notas</q-btn
              >
            </div>

            <!-- eslint-disable-next-line vue/no-v-html -->
            <div class="text-black no-margin-body" v-html="prop.node.notes" />
          </div>
        </template>

        <template #default-header="prop">
          <div class="row items-center">
            <div class="text-weight-bold text-black">{{ prop.node.label }}</div>
          </div>
        </template>

        <template #default-body="prop">
          <div class="text-black no-margin-body" style="white-space: pre-wrap">
            {{ prop.node.data }}
          </div>
        </template>
      </q-tree>
    </div>
  </div>
</template>

<script>
import { defineComponent, computed, ref } from "vue";

import useAuthStore from "src/stores/auth";

import useRepeatersStore from "src/stores/repeaters";

function push_if_qtree(cond_and_data, label, parent) {
  if (cond_and_data) {
    parent.children.push({
      id: label + Object.keys({ parent })[0] + cond_and_data,
      label: label,
      data: cond_and_data,
    });
  }
}

function filterMethod(node, filter) {
  if (node.repeater_id !== undefined) {
    // Root node (let's match everything from the root node)
    // label: "label"
    // body: "notes"
    if (node.label.toString().toLowerCase().includes(filter.toLowerCase())) {
      return true;
    }
    if (node.notes.toString().toLowerCase().includes(filter.toLowerCase())) {
      return true;
    }
  } else {
    // Other nodes:
    // label: "label"
    // body: "data"
    if (node.label.toString().toLowerCase().includes(filter.toLowerCase())) {
      return true;
    }
    if (
      node.data !== undefined &&
      node.data.toString().toLowerCase().includes(filter.toLowerCase())
    ) {
      return true;
    }
  }
  return false;
}

export default defineComponent({
  name: "RepeatersList",
  setup() {
    const authStore = useAuthStore();

    const filter = ref("");
    const filterRef = ref(null);

    const repeatersStore = useRepeatersStore();

    const repeatersAsQtree = computed(() => {
      return repeatersStore.repeaters.map(function (repeater) {
        // Prepare the bits to compose the object
        let repeater_node = {
          // q-tree root node
          id: repeater.callsign + repeater.id,
          repeater_id: repeater.id,
          icon: "cell_tower",
          label: repeater.callsign,

          // Data
          notes: repeater.notes,

          // q-tree children nodes
          children: [],

          // Style
          header: "repeater",
          body: "repeater",

          // Badges
          badge_on: false,
          badge_off: false,
          badge_project: false,
          badge_problems: false,
          badge_other: false,
          badge_simplex: false,
          badge_half_duplex: false,
          badge_2m: false,
          badge_70cm: false,
          badge_fm: false,
          badge_dstar: false,
          badge_fusion: false,
          badge_dmr: false,
        };

        // Status badges
        if (repeater.status == "OFF") repeater_node.badge_off = true;
        else if (repeater.status == "ON") repeater_node.badge_on = true;
        else if (repeater.status == "PROJECT")
          repeater_node.badge_project = true;
        else if (repeater.status == "PROBLEMS")
          repeater_node.badge_problems = true;
        else repeater_node.badge_other = true;

        // Create the location child node
        if (repeater.info_location) {
          let info_location = {
            id: repeater_node.id + "location" + repeater.info_location.id,
            label: "Localização",
            children: [],
          };

          let region_name = "Outra (não Portugal ou não especificado)";
          if (repeater.info_location.region === "CPT") {
            region_name = "Portugal Continental";
          } else if (repeater.info_location.region === "AZR") {
            region_name = "Açores";
          } else if (repeater.info_location.region === "MDA") {
            region_name = "Madeira";
          }

          push_if_qtree(region_name, "Região", info_location);
          push_if_qtree(
            repeater.info_location.latitude,
            "Latitude",
            info_location
          );
          push_if_qtree(
            repeater.info_location.longitude,
            "Longitude",
            info_location
          );
          push_if_qtree(repeater.info_location.place, "Local", info_location);
          push_if_qtree(
            repeater.info_location.qth_loc,
            "QTH loc.",
            info_location
          );

          repeater_node.children.push(info_location);
        }

        // Create the holder child node
        let info_holder = {
          id: repeater_node.id + "holder" + repeater_node.id,
          label: "Titular",
          data: null,
          children: [],
        };

        if (repeater.info_holder) {
          info_holder.data = repeater.info_holder.name
            ? repeater.info_holder.name + " (" + repeater.info_holder.abrv + ")"
            : repeater.info_holder.abrv;

          push_if_qtree(repeater.info_holder.sysop, "Sysop.", info_holder);

          repeater_node.children.push(info_holder);
        }

        // Create the modulation child node
        let modulation_node = {
          id: repeater_node.id + "modulation_nodes" + repeater_node.id,
          label: "Modulação",
          children: [],
        };

        // Check what modes the repeater has:
        if (repeater.info_fm) {
          repeater_node.badge_fm = true;
          let info_fm = {
            id: repeater_node.id + "info_fm" + repeater.info_fm.id,
            label: "FM",
            children: [],
          };

          push_if_qtree(repeater.info_fm.modulation, "Modulação", info_fm);
          push_if_qtree(repeater.info_fm.tone, "Tom", info_fm);

          modulation_node.children.push(info_fm);
        }
        if (repeater.info_dstar) {
          repeater_node.badge_dstar = true;
          const info_dstar = {
            id: repeater_node.id + "info_dstar" + repeater.info_dstar.id,
            label: "D-STAR",
            children: [],
          };

          push_if_qtree(
            repeater.info_dstar.modulation,
            "Modulação",
            info_dstar
          );
          push_if_qtree(repeater.info_dstar.gateway, "Gateway", info_dstar);
          push_if_qtree(repeater.info_dstar.reflector, "Reflector", info_dstar);

          modulation_node.children.push(info_dstar);
        }
        if (repeater.info_fusion) {
          repeater_node.badge_fusion = true;
          let info_fusion = {
            id: repeater_node.id + "info_fusion" + repeater.info_fusion.id,
            label: "Fusion (C4FM)",
            children: [],
          };

          push_if_qtree(
            repeater.info_fusion.modulation,
            "Modulação",
            info_fusion
          );
          push_if_qtree(repeater.info_fusion.wiresx, "WIRES-X", info_fusion);
          push_if_qtree(repeater.info_fusion.room_id, "Sala", info_fusion);

          modulation_node.children.push(info_fusion);
        }
        if (repeater.info_dmr) {
          repeater_node.badge_dmr = true;
          let info_dmr = {
            id: repeater_node.id + "info_dmr" + repeater.info_dmr.id,
            label: "DMR",
            children: [],
          };

          push_if_qtree(repeater.info_dmr.modulation, "Modulação", info_dmr);
          push_if_qtree(repeater.info_dmr.dmr_id, "ID DMR", info_dmr);
          push_if_qtree(repeater.info_dmr.color_code, "C.C.", info_dmr);
          push_if_qtree(
            repeater.info_dmr.ts_configuration,
            "Configuração das Time Slots",
            info_dmr
          );

          modulation_node.children.push(info_dmr);
        }

        repeater_node.children.push(modulation_node);

        if (repeater.info_simplex) {
          if (
            parseInt(repeater.info_simplex.freq_mhz) >= 144 &&
            parseInt(repeater.info_simplex.freq_mhz) <= 146
          ) {
            repeater_node.badge_2m = true;
          }
          if (
            parseInt(repeater.info_simplex.freq_mhz) >= 430 &&
            parseInt(repeater.info_simplex.freq_mhz) <= 440
          ) {
            repeater_node.badge_70cm = true;
          }

          repeater_node.badge_simplex = true;
          let info_simplex = {
            id: repeater_node.id + "info_simplex" + repeater.info_simplex.id,
            label: "RF: Simplex",
            children: [],
          };

          push_if_qtree(
            repeater.info_simplex.freq_mhz,
            "Freq. (MHz)",
            info_simplex
          );
          push_if_qtree(repeater.info_simplex.channel, "Canal", info_simplex);
          push_if_qtree(repeater.pwr_w, "Potência. (W)", info_simplex);

          repeater_node.children.push(info_simplex);
        }

        if (repeater.info_half_duplex) {
          if (
            parseInt(repeater.info_half_duplex.tx_mhz) >= 144 &&
            parseInt(repeater.info_half_duplex.tx_mhz) <= 146
          ) {
            repeater_node.badge_2m = true;
          }
          if (
            parseInt(repeater.info_half_duplex.tx_mhz) >= 430 &&
            parseInt(repeater.info_half_duplex.tx_mhz) <= 440
          ) {
            repeater_node.badge_70cm = true;
          }
          repeater_node.badge_half_duplex = true;
          let info_half_duplex = {
            id:
              repeater_node.id +
              "info_half_duplex" +
              repeater.info_half_duplex.id,
            label: "RF: Semi-duplex",
            children: [],
          };

          push_if_qtree(
            repeater.info_half_duplex.tx_mhz,
            "Tx (MHz)",
            info_half_duplex
          );
          push_if_qtree(
            repeater.info_half_duplex.rx_mhz,
            "Rx (MHz)",
            info_half_duplex
          );
          push_if_qtree(
            repeater.info_half_duplex.shift,
            "Shift (MHz)",
            info_half_duplex
          );
          push_if_qtree(
            repeater.info_half_duplex.channel,
            "Canal",
            info_half_duplex
          );
          push_if_qtree(repeater.pwr_w, "Potência (W)", info_half_duplex);

          repeater_node.children.push(info_half_duplex);
        }

        return repeater_node;
      });
    });

    return {
      filterMethod,
      authStore,
      filter,
      filterRef,
      resetFilter() {
        filter.value = "";
        filterRef.value.focus();
      },
      repeatersAsQtree,
    };
  },
});
</script>
