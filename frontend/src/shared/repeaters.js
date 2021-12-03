import { reactive } from "vue";
import axios from "axios";

export default reactive({
  repeaters: Array,
  route_query: Object,
  api_query: Object,

  updateRepeaters() {
    axios
      .get("/api/v1/repeaters/", { params: this.api_query })
      .then((res) => {
        this.repeaters = res.data;
      })
      .catch((err) => {
        console.log(err);
      });
  },
});
