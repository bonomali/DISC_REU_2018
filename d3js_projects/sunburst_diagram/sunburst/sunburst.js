var width = 960,
    height = 600,
    radius = (Math.min(width, height) / 2) - 10;

var formatNumber = d3.format(",d");

var x = d3.scaleLinear()
    .range([0, 2 * Math.PI]);

var y = d3.scaleSqrt()
    .range([0, radius]);

var color = d3.scaleOrdinal(d3.schemeCategory20c);

var partition = d3.partition();

var arc = d3.arc()
    .startAngle(function(d) { return Math.max(0, Math.min(2 * Math.PI, x(d.x0))); })
    .endAngle(function(d) { return Math.max(0, Math.min(2 * Math.PI, x(d.x1))); })
    .innerRadius(function(d) { return Math.max(0, y(d.y0)); })
    .outerRadius(function(d) { return Math.max(0, y(d.y1)); });

var sequence = 	d3.select("#active_sequence").append("svg")
	.attr("width" , 1000)
	.attr("height" , 50)


var svg = d3.select("#sunburst").append("svg")
    .attr("width", width)
    .attr("height", height)
  .append("g")
    .attr("transform", "translate(" + width / 2 + "," + (height / 2) + ")");

d3.json("sunburst_data.json", function(error, root) {
  if (error) throw error;
  
  root = d3.hierarchy(root);
  root.sum(function(d) { return d.size; });
  svg.selectAll("path")
      .data(partition(root).descendants())
    .enter().append("path")
      .attr("d", arc)
      .style("fill", function(d) { return color(d.data.name); })
      .on("click", click)
	  .on("mouseover" , mouseover)
	  .on("mouseout" , mouseleave)
    .append("title")
      .text(function(d) { return d.data.name + "\n" + formatNumber(d.value); });
});

function click(d) {
  svg.transition()
      .duration(750)
      .tween("scale", function() {
        var xd = d3.interpolate(x.domain(), [d.x0, d.x1]),
            yd = d3.interpolate(y.domain(), [d.y0, 1]),
            yr = d3.interpolate(y.range(), [d.y0 ? 20 : 0, radius]);
        return function(t) { x.domain(xd(t)); y.domain(yd(t)).range(yr(t)); };
      })
    .selectAll("path")
      .attrTween("d", function(d) { return function() { return arc(d); }; });
}

d3.select(self.frameElement).style("height", height + "px");// mouse over effects: highlight, display sequences

// Mouse over effects
function mouseover(d) {

	// display on screen the current sequence
	node = d;
	while(node.parent){
		// add rectangles
		sequence.append("rect")
			.attr("id" , "active_sequence_data")
			.attr("width" , 100)
			.attr("height" , 50)
			.style("fill", function(e) { return color(node.data.name); })
			.attr("transform" , function(e){ return "translate(" + (node.depth * 100 - 100) + ", 0)"})
		// add text
		sequence.append("text")
			.attr("id" , "active_sequence_data")
    		.attr("x", function(e) { return node.depth * 100 - 50; })
    		.attr("y", 25)
    		.attr("dy", ".35em")
    		.text(function(e) { return node.data.name; });
		
		node = node.parent;
	}
	
}

// clear mouse over effects
function mouseleave(d) {
	d3.selectAll("#active_sequence_data").remove();
}

