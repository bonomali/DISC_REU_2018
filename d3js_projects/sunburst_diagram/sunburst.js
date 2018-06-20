// Referencing Sequences Sunburst (d3 v4) by Kerry Rodden
// 		https://bl.ocks.org/kerryrodden/766f8f6d31f645c39f488a0befa1e3c8

// Vars and constants
var margin = { "top":5 , "bottom":5 , "left":5 , "right":5 },
	width  = 600 - margin.left - margin.right,
	height = 600 - margin.top - margin.bottom,
	radius = Math.min(width , height) / 2;

// Total size of all segments; we set this later, after loading the data.
var totalSize = 0; 

// adds the svg element
var vis = d3.select("#sunburst").append("svg:svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
    .append("svg:g")
    .attr("id", "container")
    .attr("transform", "translate(" + width / 2 + "," + height / 2 + ")");

// ??????
var partition = d3.partition()
    .size([2 * Math.PI, radius * radius]);

// creates an arc
var arc = d3.arc()
    .startAngle(function(d) { return d.x0; })
    .endAngle(function(d) { return d.x1; })
    .innerRadius(function(d) { return Math.sqrt(d.y0); })
    .outerRadius(function(d) { return Math.sqrt(d.y1); });
