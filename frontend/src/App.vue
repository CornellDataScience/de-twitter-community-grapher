<template>
  <div>
  <img alt="Vue logo" src="./assets/logo.png" />
  <input v-model="name">
  <button v-on:click="set(name)"> enter </button>
  <div>
    <p> {{ name }} </p>
  </div>
  <HelloWorld msg="Welcome to Your Vue.js + TypeScript App" />
  </div>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import HelloWorld from "./components/HelloWorld.vue";

export default defineComponent({
  name: "App",
  components: {
    HelloWorld
  },
  data() {
    return {
      name: undefined,
      test2: "undefined"
    }
  },
  methods: {
    set: function (name: string) {
      alert(name);
    }
  }
});
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
