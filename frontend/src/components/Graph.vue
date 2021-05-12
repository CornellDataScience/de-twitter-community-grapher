<template>

  <div>

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
    computed: {
      userData: function() {
        return this.$store.getters.getUserData;
      }
    },
    watch: {
      userData: function(value) {

        const graphData = value;

        const svg = d3.select('svg')
        const width = svg.attr('width')
        const height = svg.attr('height')

        svg.selectAll('*').remove();

        let nodes = graphData.vertices;
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
      
        let links = graphData.edges;
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




