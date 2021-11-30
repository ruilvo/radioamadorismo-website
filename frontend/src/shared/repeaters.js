import { reactive } from "vue";
import axios from "axios";

export default reactive({
  repeaters: Array,
  isBusy: false,

  getRepeaters(params = {}) {
    this.isBusy = true;
    axios
      .get("/api/v1/repeaters/", { params: params })
      .then((res) => {
        this.repeaters = res.data;
      })
      .catch((err) => {
        console.log(err);
      })
      .finally(() => (this.isBusy = false));
  },
});
