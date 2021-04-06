<template>
  <div>
    <h1>{{ user }}</h1>
  </div>
</template>

<script lang="ts">

import { defineComponent } from "vue";

export default defineComponent({
  name: "Graph",
  props: ["user"]
});

</script>
