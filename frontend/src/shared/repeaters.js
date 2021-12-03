import { reactive } from "vue";
import axios from "axios";

export default reactive({
  repeaters: Array,
  route_query: Object,

  updateRepeaters(params = {}) {
    axios
      .get("/api/v1/repeaters/", { params: params })
      .then((res) => {
        this.repeaters = res.data;
      })
      .catch((err) => {
        console.log(err);
      });
  },
});
