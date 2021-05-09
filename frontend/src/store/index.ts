import { createStore } from "vuex";

const url = "http://localhost:5001/api/graph?name=";
const  headers = { Accept: "application/json" };

export default createStore({
  state: {
    userData: {},
  },
  mutations: {
    setUserData (state, data) {
      state.userData = data
    }
  },
  actions: {
    async setUserData (state, userHandle) {
      const data = await fetch(url+userHandle, {
        mode: "no-cors"
      }).then(response => response.json());
      state.commit("setUserData", data);
    }

  },
  modules: {

  },
  getters: {
    getUserData(state) {
      return state.userData
    }
  }

});
