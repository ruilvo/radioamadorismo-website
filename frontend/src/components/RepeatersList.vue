<template>
  <div class="text-h6">Lista de repetidores</div>
  <div class="col">
    <q-tree :nodes="repeatersAsQtree" node-key="id">
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
        <div class="text-black no-margin-body" style="white-space: pre-wrap">
          {{ prop.node.notes }}
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

    <q-btn
      color="primary"
      class="full-width q-mt-md"
      :disable="repeatersAsQtree.length >= repeatersStore.count"
      @click="loadMore"
      >Mostrando {{ repeatersAsQtree.length }} de {{ repeatersStore.count }} na
      base de dados. Clique aqui para carregar mais.</q-btn
    >
  </div>
</template>

<script>
import { defineComponent, computed } from "vue";

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

export default defineComponent({
  name: "RepeatersList",
  setup() {
    const repeatersStore = useRepeatersStore();

    const repeatersAsQtree = computed(() => {
      return repeatersStore.repeaters.map(function (repeater) {
        // Prepare the bits to compose the object
        var repeater_node = {
          // q-tree root node
          id: repeater.callsign + repeater.id,
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
          badge_simplex: false,
          badge_half_duplex: false,
          badge_fm: false,
          badge_dstar: false,
          badge_fusion: false,
          badge_dmr: false,
        };

        // Create the location child node
        if (repeater.info_location) {
          var info_location = {
            id: repeater_node.id + "location" + repeater.info_location.id,
            label: "Localização",
            children: [],
          };

          var region_name = "Outra (não Portugal ou não especificado)";
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
        var info_holder = {
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
        var modulation_node = {
          id: repeater_node.id + "modulation_nodes" + repeater_node.id,
          label: "Modulação",
          children: [],
        };

        // Check what modes the repeater has:
        if (repeater.info_fm) {
          repeater_node.badge_fm = true;
          var info_fm = {
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
          var info_fusion = {
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
          var info_dmr = {
            id: repeater_node.id + "info_dmr" + repeater.info_dmr.id,
            label: "DMR",
            children: [],
          };

          push_if_qtree(repeater.info_dmr.modulation, "Modulação", info_dmr);
          push_if_qtree(repeater.info_dmr.dmr_id, "ID DMR", info_dmr);
          push_if_qtree(repeater.info_dmr.color_code, "C.C.", info_dmr);
          push_if_qtree(
            repeater.info_dmr.ts1_configuration,
            "T.S. 1",
            info_dmr
          );
          push_if_qtree(
            repeater.info_dmr.ts2_configuration,
            "T.S. 2",
            info_dmr
          );

          modulation_node.children.push(info_dmr);
        }

        repeater_node.children.push(modulation_node);

        if (repeater.info_simplex) {
          repeater_node.badge_simplex = true;
          var info_simplex = {
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
          repeater_node.badge_half_duplex = true;
          var info_half_duplex = {
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
      repeatersAsQtree,
      repeatersStore,
      loadMore() {
        repeatersStore.updateRepeaters(
          repeatersStore.lastOffset + repeatersStore.lastLimit,
          repeatersStore.lastLimit,
          true
        );
      },
    };
  },
});
</script>
