import { reactive } from "vue";
import axios from "axios";

export default reactive({
  repeaters: [],
  query: {},

  updateRepeaters() {
    axios
      .get("/api/v1/repeaters/", { params: this.query })
      .then((res) => {
        this.repeaters = res.data;
      })
      .catch((err) => {
        console.log(err);
      });
  },
});
