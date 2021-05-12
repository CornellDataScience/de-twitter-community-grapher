<template>

  <div>

    <button v-on:click="clickHandler">Create Graph</button>

    <svg width='1500' height='1000' class='arjunstest'></svg>

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
      clickHandler() {
        const svg = d3.select('svg')
        const width = svg.attr('width')
        const height = svg.attr('height')

        svg.selectAll('*').remove();

        const nodes3 = [{name: 1}, {name: 2}, {name: 3}, {name: 4}, {name: 5}, {name: 6}, {name: 7}, {name: 8}, {name: 9}, {name: 10}, {name: 11}, {name: 12}, {name: 13}]
        const links3 = [
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


        const nodes2 = [{name: 1}, {name: 2}, {name: 3}, {name: 4}, {name: 5}, {name: 6}, {name: 7}, {name: 8}, {name: 9}, {name: 10}, {name: 11}, {name: 12},
        {name: 13}, {name: 14}, {name: 15}, {name: 16}, {name: 17}, {name: 18}, {name: 19}, {name: 20}, {name: 21}, {name: 22}, {name: 23}, {name: 24},
        {name: 25}, {name: 26}, {name: 27}, {name: 28}, {name: 29}, {name: 30}]
        const links2 = [
          {source: 1, target: 2},
          {source: 2, target: 3},
          {source: 1, target: 4}, 
          {source: 4, target: 5},
          {source: 4, target: 8},
          {source: 8, target: 7},
          {source: 6, target: 7},
          {source: 5, target: 6},
          {source: 1, target: 21},
          {source: 21, target: 24},
          {source: 21, target: 22},
          {source: 22, target: 23},
          {source: 23, target: 24},
          {source: 1, target: 12},
          {source: 13, target: 12},
          {source: 13, target: 14},
          {source: 14, target: 15},
          {source: 15, target: 12},
          {source: 1, target: 9},
          {source: 9, target: 10},
          {source: 10, target: 11},
          {source: 11, target: 9},
          {source: 1, target: 20},
          {source: 20, target: 19},
          {source: 20, target: 18},
          {source: 19, target: 18},
          {source: 18, target: 17},
          {source: 17, target: 16},
          {source: 28, target: 27},
          {source: 23, target: 25},
          {source: 25, target: 26},
          {source: 25, target: 27},
          {source: 27, target: 30},
          {source: 28, target: 29},
          {source: 26, target: 29}
        ]

        const nodes4 = [{name: 1}, {name: 2}]
        const links4 = [
          {source: 1, target: 2}
        ]

        let nodes = this.userData.vertices;
        nodes = nodes.map(item => {
          return {name: parseInt(item.id), label: item.properties.name[0].value};
        });

        let linkDistance = Math.round(450 / Math.round(nodes.length/2));
        if (linkDistance < 40) {
          linkDistance = 20;
        }

        let strength = Math.round(6000 / Math.round(nodes.length/2));
        if (linkDistance == 20) {
          strength = 100;
        }

        strength = strength*-1;
      
        let links = this.userData.edges;
        links = links.map(item => {
          return {source: parseInt(item.source), target: parseInt(item.target)};
        });

        const simulation = d3.forceSimulation(nodes)
          .force('charge', d3.forceManyBody())
          .force('center', d3.forceCenter(width / 2, height / 2))
          .force('link',d3.forceLink(links).id(function(d) { return d.name;}))
          .force('link',d3.forceLink(links).distance(linkDistance))
          .force("repulse", d3.forceManyBody().strength(strength))
          
        const texts = svg.selectAll(".texts")
          .data(nodes)
          .enter()
          .append("text")
          .attr("dx", 12)
          .attr("dy", "0.35em")
          .text(function(d) { return d.label; });

        const link = svg.selectAll('line').data(links).enter()
          .append('line')
          .attr('class','link');

        const node = svg.selectAll('circle').data(nodes).enter()
          .append('circle')
          .attr('class','node')
          .attr('r', 5);

        const graph = svg.select('.graph')

        const g = svg.append("g");

        const zoomHandler = d3.zoom()
          .scaleExtent([0.1,20])
          .on('zoom', function(event) {
            console.log(event);
            node.attr('transform', event.transform);
            link.attr('transform', event.transform);
            texts.attr('transform', event.transform);
          });
        
        zoomHandler(svg);

        function ticked() {
          link.attr('x1', function(d) { return d.source.x; })
            .attr('y1', function(d) { return d.source.y; })
            .attr('x2', function(d) { return d.target.x; })
            .attr('y2', function(d) { return d.target.y; })
            .merge(link);

          node.attr('cx', function(d) { return d.x; })
            .attr('cy', function(d) { return d.y; })
            .merge(node);

          texts.attr("x", function(d) { return d.x;})
               .attr("y", function(d) { return d.y});

        }

        function clamp(x, lo, hi) {
          return x < lo ? lo : x > hi ? hi : x;
        }

        const nodeDrag = d3.drag()
          .on("start", function(event,d) {
            d3.select(this).classed("fixed", true);
          }).on("drag", function(event,d) {
            d.fx = clamp(event.x, 0, width);
            d.fy = clamp(event.y, 0, height);
            simulation.alpha(1).restart();
          });

        node.call(nodeDrag)

        simulation.on('tick',ticked)

      }
    },
    computed: {
      userData() {
        return this.$store.getters.getUserData;
      }
    }
  });

</script>

<style>
  .node {
    fill: rgb(255, 0, 0);
    stroke-width: 2px;
  }

  text {
    pointer-events: none;
    font: 10px sans-serif;
  }

  .link {
    stroke: rgb(0, 0, 0);
    stroke-width: 1px;
  }

  
</style>




