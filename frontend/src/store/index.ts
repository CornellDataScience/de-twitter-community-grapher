import { createStore } from "vuex";

const url = "";
const  headers = { Accept: "application/json" };

export default createStore({
  state: {
    userData: []
  },
  mutations: {
    setUserData (state, data) {
      state.userData = data
    }
  },
  actions: {
    async setUserData (state) {
      const data = await fetch(url, { headers} )
      const d = await data.json();
      state.commit("setUserData", data)
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
