<template>
  <div>
  <input v-model="handle">
  <button v-on:click="send(handle)"> enter </button>
  <p> {{ user }} </p>
  </div>

  <p>
    <span id="output">

    </span>
  </p>
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
      user: 'hello'
    }
  }, 
  methods: {
    send: function(handle: string) {
      document.getElementById('output').innerHTML = handle
    },
  },
});
</script>
