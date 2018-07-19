// adjust scope for full webpage
function makeSunburst(){

const INPUT_FILE = "json_files/sunburst_data_struc2vec.json"

// Set up variables
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

// center pie chart
var pieChart = d3.pie().value(function(d) { return 5; });

var sequence = 	d3.select("#active_sequence").append("svg")
	.attr("width" , 1000)
	.attr("height" , 50)

// add svg element
var svg = d3.select("#sunburst_diagram").append("svg")
    .attr("width", width)
    .attr("height", height)
  .append("g")
    .attr("transform", "translate(" + width / 2 + "," + (height / 2) + ")");

// load in data
d3.json(INPUT_FILE, function(error, root) {
  
  if (error) throw error;
  
  root = d3.hierarchy(root);

  root.sum(function(d) { return d.size; });
  svg.selectAll("path")
      .data(partition(root).descendants())
    .enter().append("path")
	  .attr("id" , "sun_path")
      .attr("d", arc )
      .style("fill", function(d) { return color(d.data.name); })
      .on("click", click)
	  .on("mouseover" , mouseover)
	  .on("mouseout" , mouseleave)
    .append("title")
      .text(function(d) { return d.data.name + "\n" + formatNumber(d.value); });
});

function click(d) {

	// zoom in feature
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

	//~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	// clear data table
	d3.select("#scrollable-content").select("table").select("tbody").selectAll("tr").remove();
	
	// fill in data table
	
	// display name of sequence
	var name_seq = "";
	d3.select("#node_sequence")
		.text( function(e){ 
			var node = d;
			while(node.parent){
				name_seq = node.data.name + "-" + name_seq;
				node = node.parent;
			}
			if(name_seq[ name_seq.length - 1 ] === "-")
				name_seq = name_seq.slice(0, -1);
			return name_seq; 
		});


	// use the sequence name to find matches
	// then display in scrollable content
	d3.csv("sequence.csv" , function(input){
		var matching = [];

		// add the matching people to the array
		input.forEach( function(object){

			var seq_indices = getIndicesOf(name_seq , object.sequence);

			if( seq_indices.length > 0 ){
				newObj = object;
				newObj.num_seq = seq_indices.length;
				
				seq_indices.forEach( function(i){
					newObj.sequence = newObj.sequence.replaceAll( name_seq , '...' )
				});


				matching.push(newObj);
			}
		});

		// display data in scrolllable table		
 		var rows = d3.select("#scrollable-content").select("table").select("tbody").selectAll("tr")
			.data(matching, function (d) {return d;});

		rows.enter()
			.append('tr')
			.selectAll("td")
			.data(function (d) {return [d.num_seq, d.sequence];})
			.enter()
			.append("td")
			.text(function(d) { return d; });

		rows.exit().remove();

		var cells = rows.selectAll('td')
			.data(function (d) {return [d.num_seq, d.sequence];})
			.text(function (d) {return d;});

		cells.enter()
			.append("td")
			.text(function(d) { return d; });

		cells.exit().remove();
	});
}

String.prototype.replaceAll = function(str1, str2, ignore) 
{
    return this.replace(new RegExp(str1.replace(/([\/\,\!\\\^\$\{\}\[\]\(\)\.\*\+\?\|\<\>\-\&])/g,"\\$&"),(ignore?"gi":"g")),(typeof(str2)=="string")?str2.replace(/\$/g,"$$$$"):str2);
} 

function getIndicesOf(searchStr, str, caseSensitive) {
    var searchStrLen = searchStr.length;
    if (searchStrLen == 0) {
        return [];
    }
    var startIndex = 0, index, indices = [];
    if (!caseSensitive) {
        str = str.toLowerCase();
        searchStr = searchStr.toLowerCase();
    }
    while ((index = str.indexOf(searchStr, startIndex)) > -1) {
        indices.push(index);
        startIndex = index + searchStrLen;
    }
    return indices;
}


// Mouse over effects
function mouseover(d) {

	// display on screen the current sequence
	var node = d;
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

		console.log(node.depth)
	}
	
}

// clear mouse over effects
function mouseleave(d) {
	d3.selectAll("#active_sequence_data").remove();
}


} // end scope for webpage

makeSunburst();
