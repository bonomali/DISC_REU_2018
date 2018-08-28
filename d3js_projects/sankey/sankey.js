function click3(name){
	var needToAdd = true;
	selected.nodes.forEach( function(node){
		if(node.name === name) needToAdd = false;
	});
	if(needToAdd && selected.nodes.length - 5 < 4){

		// select node of same name
		graph.nodes.forEach(function(node){
			
			if(node.name === name) selected.nodes.push(node);

			if(node.name == "A" && signal.A == 0) {
				selected.nodes.push(node);
				signal.A = 1;
			}
			if(node.name == "B" && signal.B == 0) {
				selected.nodes.push(node);
				signal.B = 1;
			}
			if(node.name == "C" && signal.C == 0) {
				selected.nodes.push(node);
				signal.C = 1;
			}
			if(node.name == "D" && signal.D == 0) {
				selected.nodes.push(node);
				signal.D = 1;
			}
			if(node.name == "F" && signal.F == 0) {
				selected.nodes.push(node);
				signal.F = 1;
			}
			
		});

		// select link of same name
		graph.links.forEach(function(link){
			if(link.source.name === name) selected.links.push(link);
		});
		
	}
	if(!needToAdd && flag==true){
		for(let i = selected.nodes.length-1;i>=0;i--){
			if(selected.nodes[i].name === name)
				selected.nodes.splice(i,1);
		}
		for(let i = selected.links.length-1;i>=0;i--){
			if(selected.links[i].source.name === name)
				selected.links.splice(i,1);
		}
		draw(selected);
		return;
	}
	draw(selected);
	link3.attr("stroke-opacity", function(d){
		if (d.source.name === name )
			return 0.5;
		else
			return 0.2;
	});
	
	if(flag === true){
		flag=false;
//----------------find the node in graph 1---------------------//
		node.attr("r",function(k){
			if(k.id == name){
				main_node = k;
				pool.push(k);
			}
			return 5;
		});
		save.length = 0;
		click1(pool[0]);
		pool.length = 0;
//----------------find the node in graph 2---------------------//
		var p = name2path(name);
		if(p){
			mouseover(p);
			click2(p);
		}
		flag=true;
	}
}

function draw(data){
	svg3.selectAll("g").remove();
	var sankey = d3.sankey()
		.nodeWidth(75)
		.nodePadding(25)
		.size([380, 200]);
	path3 = sankey.link();
	sankey
      .nodes(data.nodes)
      .links(data.links)
      .layout(32);

  // add in the links
	link3 = svg3.append("g").selectAll(".link")
      .data(data.links)
	  .enter().append("path")
      .attr("class", "link")
      .attr("d", path3)
	  .attr("stroke-opacity", 0.2)
      .style("stroke-width", function(d) { return Math.max(1, d.dy); })
      .sort(function(a, b) { return a.dy - b.dy; });
	

  // add the link titles
  link3.append("title")
        .text(function(d) {
    		return d.source.name + " → " + 
                d.target.name + "\n" + format(d.value); });

  // add in the nodes
  var node = svg3.append("g").selectAll(".node")
      .data(data.nodes)
      .enter().append("g")
      .attr("class", "node")
      .attr("transform", function(d) { 
		  return "translate(" + d.x + "," + d.y + ")"; })
      .call(d3.drag()
        .subject(function(d) {
          return d;
        })
        .on("start", function() {
          this.parentNode.appendChild(this);
        })
        .on("drag", dragmove))
		.on("click", function(d){ click3(d.name); })

  // add the rectangles for the nodes
  node.append("rect")
      .attr("height", function(d) { return d.dy; })
      .attr("width", sankey.nodeWidth())
      .style("fill", function(d){
		  return d.color = color3(d.name.replace(/ .*/, ""));
		})
      .style("stroke", function(d) { 
		  return d3.rgb(d.color).darker(2); })
      .append("title")
      .text(function(d) { 
		  return d.url + "\n" + format(d.value); });


  // add in the title for the nodes
  var text= node.append("text")
      .attr("x", sankey.nodeWidth())
      .attr("y", function(d) { return d.dy / 2; })
      .attr("dy", function(d) { return d.dy / 2;})
      .attr("text-anchor", "end")
      .attr("transform", null)
      .text(function(d) { 
		switch(d.name){
			case "A":
				return "1.0";
			case "B":
				return "0.90-0.99";
			case "C":
				return "0.80-0.89";
			case "D":
				return "0.70-0.79";
			case "F":
				return "0.00-0.69";
			default:
				return d.name;
		}
	  })
      .filter(function(d) { return d.x < width / 2; });

	function dragmove(d) {
		d3.select(this)
        .attr("transform", "translate(" + d.x + "," + (d.y = Math.max(0, Math.min(height - d.dy, d3.event.y)) ) + ")");
		sankey.relayout();
		link.attr("d", path);
    }
}
var graph = {"nodes" : [], "links" : []};;
var	selected = { "nodes":[] , "links":[] };

var margin = {top: 10, right: 10, bottom: 10, left: 10},
    width = 400 - margin.left - margin.right,
    height = 250;
var svg3 = d3.select("#sankey_diagram").append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height)
    .append("g")
    .attr("transform", 
          "translate(" + margin.left + "," + margin.top + ")");
var path3;
var link3;
var signal = {"A":0,"B":0,"C":0,"D":0,"F":0};
var units = "Students";
var formatNumber = d3.format(",.0f"),    // zero decimal places
    format = function(d) { return formatNumber(d) + " " + units; };
var color3 = d3.scaleOrdinal(d3.schemeCategory20); 

function makeSankeyD3V4(){

var sankey_data = "csv_files/dummy_grades_v2.csv";
var url_file = "csv_files/object_ref_v2.csv";
// load the data
d3.csv(url_file, function(e , url_data){
d3.csv(sankey_data, function(error, data) {
 
	//~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  	//set up graph in same style as original example but empty
	graph = {"nodes" : [], "links" : []};

  	data.forEach(function (d) {
    	graph.nodes.push({ "name": d.source});
    	graph.nodes.push({ "name": d.target});
    	graph.links.push({ "source": d.source,
        	               "target": d.target,
            	           "value": +d.value });
   	});

  	// return only the distinct / unique nodes
  	graph.nodes = d3.keys(d3.nest().key(function (d) { return d.name; })
    	.object(graph.nodes));

  	// loop through each link replacing the text with its index from node
  	graph.links.forEach(function (d, i) {
  		graph.links[i].source = graph.nodes.indexOf(graph.links[i].source);
    	graph.links[i].target = graph.nodes.indexOf(graph.links[i].target);
  	});

  	// now loop through each nodes to make nodes an array of objects
  	// rather than an array of strings
	graph.nodes.forEach(function (d, i) {
		var url_name = "";
		var arr = d.replace('|','.').split('.');
		arr.reverse();
		arr.forEach(function(number){
			url_data.forEach(function(line){
				if(line.num == number)
					url_name = url_name + line.url + '-->';
			});
		});
		url_name = url_name.slice(0,-3);
		graph.nodes[i] = { "name": d, "url":url_name };
	});
  	

	//~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	// sequence selector
	
	// make an array of sequences from data
	var sequences = [];

	graph.nodes.forEach( function(node){

		// add all nodes that aren't grades to an array
		switch(node.name){

			// filter out the grade nodes
			case "A": break;
			case "B": break;
			case "C": break;
			case "D": break;
			case "F": break;

			// add all sequences to array
			default:
				sequences.push( node.name )
				break;
		}
	});
	sequences.sort(function(a,b){ return a>b?true:false; });
	var special = ["18|37.13", "37|12", "18|36.18.37.29","18|37.12","37|13","36|6.34"]
	// add buttons to sequence selector
	var data_buttons = d3.select("#sankey_button").selectAll("button")
		.data(sequences).enter()
		.append("button")
			.attr("class" , "sankey_sequence")
			.style("background", function(d){
				var sig = false;
				special.forEach(function(name){if(name===d) sig=true; });
				if(sig===true){
					return "red";
				}
				else
					return "white";
			})
			.text(d => d);


	data_buttons.on("click" , click3);

	/********************************************************************
	 * DON'T FORGET TO ADD GRADES NODES AND LINKS TO SELECTED
	 * ******************************************************************/
	
  //~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	draw(graph);
	var i;
	flag = false;
	for(i = 0;i < 3;i+=1){
		var r = Math.floor(Math.random()*502);
		click3(graph.nodes[r].name);
	}
	flag = true;
	draw(selected);
	selected.nodes.length = 0;
	selected.links.length = 0;
	signal.A = 0;
	signal.B = 0;
	signal.C = 0;
	signal.D = 0;
	signal.F = 0;
	
});

});
}
makeSankeyD3V4();
//~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

