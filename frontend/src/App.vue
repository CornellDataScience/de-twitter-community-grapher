<template>
  <div>

  <h1 id="title">Welcome to Twitter Community Grapher</h1><br><br>

  <div id="userInputs">
    <h2>Enter a Twitter Handle</h2>

    <input v-model="handle" id="textbox"> <br> <br>
    <div class="button">
      <button v-on:click="fetchData(handle)"> Create Graph </button>
    </div>
    
  </div>
  
  <Graph v-bind:user="user" />
  </div>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import Graph from "./components/Graph.vue";

export default defineComponent({
  name: "App",
  components: {
    Graph
  },
  methods: {
    fetchData(handle) {
      this.$store.dispatch("setUserData", handle);
    }
  },
  data() {
    return {
      user: ''
    }
  } 
});
</script>

<style>
  #title {
    font-size: 50px;
    font-family: 'Palatino';
    text-align: center;
    background-color: rgb(29, 161, 242);
  }

  #userInputs {
    text-align: center;
    font-family: 'Palatino';
  }

  body {
    background-color: lightblue;
  }
</style>
