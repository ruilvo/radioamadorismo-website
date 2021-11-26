import { reactive } from "vue";
import axios from "axios";

export default reactive({
  repeaters: Array,
  isBusy: false,

  async getRepeaters() {
    this.isBusy = true;
    axios
      .get("/api/v1/repeaters/")
      .then((res) => {
        this.repeaters = res.data;
      })
      .catch((err) => {
        console.log(err);
      })
      .then(() => (this.isBusy = false));
  },
});
