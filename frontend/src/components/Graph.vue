<template>

  <div>
    <h1>{{user}}</h1>

    <svg width='500' height='500' class='arjuns test'></svg>

  </div>

</template>

<script lang="ts">

import * as d3 from "d3";
import { defineComponent } from "vue";

  export default defineComponent({
    name: "Graph",
    data: function() {
      return {
        
      }
    },
    props: ["user"],
    methods: {
       
    },
    computed: {
      userData() {
        return this.$store.getters.getUserData;
      }
    },
    mounted() {
      const svg = d3.select('svg')
      const width = svg.attr('width')
      const height = svg.attr('height')

      const nodes = [{name: 0}, {name: 1}, {name: 2}, {name: 3}, {name: 4}, {name: 5}, {name: 6}]
      
      const links = [
        {source: 0, target: 1},
        {source: 0, target: 2},
        {source: 1, target: 5},
        {source: 2, target: 3},
        {source: 2, target: 6},
        {source: 5, target: 4},
        {source: 3, target: 6},
        {source: 1, target: 4}
      ]

      const simulation = d3.forceSimulation(nodes)
        .force('charge', d3.forceManyBody())
        .force('center', d3.forceCenter(width / 2, height / 2))
        .force('link',d3.forceLink(links).id(function(d) { return d.name;}))
            
      function ticked() {

        const node = d3.select('svg')
          .selectAll('circle')
          .data(nodes)

        const link = d3.select('svg')
          .selectAll('line')
          .data(links)

        link.enter()
          .append('line')
          .merge(link)
          .attr('class','link')
          .attr('x1', function(d) { return d.source.x; })
          .attr('y1', function(d) { return d.source.y; })
          .attr('x2', function(d) { return d.target.x; })
          .attr('y2', function(d) { return d.target.y; })

        node.enter()
          .append('circle')
          .attr('class','node')
          .attr('r', 5)
          .merge(node)
          .attr('cx', function(d) { return d.x; })
          .attr('cy', function(d) { return d.y; })

        node.append("title")
          .text(function(d) { return d.name });

        }

      simulation.on('tick',ticked)

    } 
  });

</script>

<style>
  .node {
    fill: rgb(255, 0, 0);
    stroke-width: 2px;
  }

  .node text {
    pointer-events: none;
    font: 10px sans-serif;
  }

  .link {
    stroke: rgb(0, 0, 0);
    stroke-width: 1px;
  }
  
</style>



