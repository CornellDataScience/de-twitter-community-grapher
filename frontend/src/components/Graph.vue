<template>

  <div>
    <h1>Test</h1>

    <svg width='500' height='500' class='arjuns test'>

    </svg>

  </div>

</template>

<script lang="ts">

import * as d3 from "d3";
import { defineComponent } from "vue";

  export default defineComponent({
    name: "Graph",
    props: ["user"],
    methods: {
       
    },
    mounted() {
    const svg = d3.select('svg')
    const width = svg.attr('width')
    const height = svg.attr('height')

    console.log(width);
    console.log(height);

    const nodes = [{}, {}, {}, {}, {}, {}, {}, {}, {}]

      const links = [
          {source: 'node1', target: 'node2'},
          {source: 'node1', target: 'node3'},
          {source: 'node2', target: 'node3'},
      ]

      function ticked() {
        const u = d3.select('svg')
          .selectAll('circle')
          .data(nodes)

        u.enter()
          .append('circle')
          .attr('r', 5)
          .merge(u)
          .attr('cx', function(d) {
            return d.x
          })
          .attr('cy', function(d) { 
            return d.y
          })

        u.exit().remove()
      }


      const simulation = d3.forceSimulation(nodes)
  .force('charge', d3.forceManyBody())
  .force('center', d3.forceCenter(width / 2, height / 2))
  .on('tick', ticked);

  simulation.force('charge', d3.forceManyBody())

  /*
      function ticked(e) {

        node.attr('cx', function(d) { return d.x; })
          .attr('cy', function(d) { return d.y; })
          .call(force.drag);

        link.attr('x1', function(d) { return d.source.x; })
          .attr('y1', function(d) { return d.source.y; })
          .attr('x2', function(d) { return d.target.x; })
          .attr('y2', function(d) { return d.target.y; })
      }
      */

      
    },
    data: function() {
      return {

      }
    }
      
  });


</script>

<style>
  .node {
    fill: #ccc;
    stroke: #fff;
    stroke-width: 2px;
  }

  .link {
    stroke: #777;
    stroke-width: 2px;
  }
  
</style>

