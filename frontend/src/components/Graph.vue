<template>

  <div>
    <h1>{{user}}</h1>

    <button v-on:click="clickHandler">test</button>

    <svg width='500' height='500' class='arjuns test'></svg>

  </div>

</template>d

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
      clickHandler() {
        console.log(this.userData)
        const svg = d3.select('svg')
        const width = svg.attr('width')
        const height = svg.attr('height')

        const nodes = [{name: 1}, {name: 2}, {name: 3}, {name: 4}, {name: 5}, {name: 6}, {name: 7}, {name: 8}, {name: 9}, {name: 10}, {name: 11}, {name: 12}, {name: 13}]
        const links = [
          {source: 1, target: 2},
          {source: 1, target: 3},
          {source: 2, target: 3}, 
          {source: 3, target: 4},
          {source: 4, target: 5},
          {source: 5, target: 6},
          {source: 6, target: 7},
          {source: 4, target: 7},
          {source: 4, target: 8},
          {source: 8, target: 9},
          {source: 9, target: 10},
          {source: 8, target: 10},
          {source: 11, target: 4},
          {source: 11, target: 12},
          {source: 11, target: 13},
          {source: 12, target: 13},
          {source: 13, target: 8}
        ]

        let nodes2 = this.userData.vertices;
        nodes2 = nodes2.map(item => {
          return {name: parseInt(item.id)};
        });
        
        console.log(this.userData.edges)
        
        let links2 = this.userData.edges;
        links2 = links2.map(item => {
          return {source: parseInt(item.source), target: parseInt(item.target)};
        });

        const simulation = d3.forceSimulation(nodes)
          .force('charge', d3.forceManyBody())
          .force('center', d3.forceCenter(width / 2, height / 2))
          .force('link',d3.forceLink(links).id(function(d) { return d.name;}))
          //.force('link',d3.forceLink(links).distance(150).strength(0.1))
          .force("repulse", d3.forceManyBody().strength(-150) )

        const texts = svg.selectAll(".texts")
          .data(nodes)
          .enter()
          .append("text")
          .attr("dx", 12)
          .attr("dy", "0.35em")
          .text(function(d) { return d.name; });
              
        function ticked() {

          const node = svg.selectAll('circle').data(nodes)

          const link = svg.selectAll('line').data(links)

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

          texts.attr("x", function(d) { return d.x;})
               .attr("y", function(d) { return d.y});

          }

        simulation.on('tick',ticked)

      }
    },
    computed: {
      userData() {
        return this.$store.getters.getUserData;
      }
    },
    mounted() {
      this.$store.dispatch("setUserData");
      

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




