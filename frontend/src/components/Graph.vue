<template>

  <div>
    <h1>{{ user }}</h1>
  </div>

  <div id="networkGraph">
    <d3-network :net-nodes="nodes" :net-links="connections" :options="options" />
  </div>


</template>

<script>
    import { defineComponent} from "vue";

    const D3Network = window.vueD3Network
    export default defineComponent({
        el:"#networkGraph",
      components: {
        D3Network
  },
  data () {
    return {
      nodes: [
        {id: 1, name: 'node1', _color: 'red'},
        {id: 2, name: 'node2', _color: 'green'},
        {id: 3, name: 'node3', _color: 'black'}
      ],
      connections: [
        { sid: 1, tid: 2 },
        { sid: 2, tid: 3 },
        { sid: 3, tid: 1 }
      ],
nodeSize:35,
    }
  },
  computed:{
    options(){
      return{
        nodeLabels: true,
        size:{ w:2000, h:1080},
        nodeSize: 35,
        force: 10000
      }
    }
  }
})
  
</script>

<!--
<script lang="ts">
import { defineComponent } from "vue";

export default defineComponent({
  name: "Graph",
  props: ["user"],  
  mounted() {
    const externalScript = document.createElement('script')
    externalScript.setAttribute('src', 'https://d3js.org/d3.v4.min.js')
    document.head.appendChild(externalScript)
  },
});

</script>
-->
