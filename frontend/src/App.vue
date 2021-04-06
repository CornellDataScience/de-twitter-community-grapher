<template>
  <div>
  <h1>Enter Twitter Handle</h1>
  <input v-model="handle"> <br> <br>
  <button v-on:click="this.user=handle"> Submit </button>
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
  data() {
    return {
      user: ''
    }
  } 
});
</script>
