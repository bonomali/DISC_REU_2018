// adjust scope for full webpage
/*	
 *	Filename: hon_fdd.js
 *	Date:	  6/21/2018
 * 	Authors:  Eric Gronda, Maggie Goulden
 *	Works Cited:
 *		Bostock, Mike. “Force-Directed Graph.” Popular Blocks, 13 June 2018, bl.ocks.org/mbostock/4062045.
 *
 *	Description:
 *		js file for the higher order network force directed diagram. 
 */

// adjust scope for interactive webpage
var node;
var link;
var Grouping = "Gephi";
var linkedByIndex = {};
var svg = d3.select("#hon_diagram").select("svg");
var defs = svg.append("svg:defs");
var color = d3.scaleOrdinal(d3.schemeCategory10);
var flag=true;
var main_node;
var clicked = false;
var save = new Array();
function click1(d){
	/* highlight travel path for nodes */

	// check all other nodes to see if they're connected
    // to this one. if so, keep the opacity at 1, otherwise
    // fade
		var sig;
		clicked = true;
		pool.forEach(function(d){
			save.push(d);
		});
		node.style("stroke-opacity", function(o) {
			sig = false;
			pool.forEach(function(k,i){
				if(isConnected(k, o)) 
					sig = true;
			});
			return sig === true? 1: 0.05;
		});
		node.style("fill-opacity", function(o) {
			sig = false;
			pool.forEach(function(k,i){
				if(isConnected(k, o)) 
					sig = true;
			});
			return sig === true? 1: 0.05;
		});
		link.style("stroke-opacity", function(o) {
			sig = false;
			pool.forEach(function(k,i){
				if(o.source === k || o.target === k) 
					sig = true;
			});
			return sig === true? 1: 0.05;
		});
		switch(Grouping) {
			case "Gephi":
      			link.attr("marker-end", function(o) {
					sig = false;
					pool.forEach(function(k,i){
						if(o.source === k || o.target === k) 
							sig = true;
					});
					return sig === true? marker(color(o.Gephi), 1.0) : marker(color(o.Gephi), 0.05);
				});
				break;
			case "D15":
				link.attr("marker-end", function(o) {
					sig = false;
					pool.forEach(function(k,i){
						if(o.source === k || o.target === k) 
							sig = true;
					});
					return sig === true? marker(color(o.Group_15D), 1.0) : marker(color(o.Group_15D), 0.05);
				});
				break;
			case "D2":
				link.attr("marker-end", function(o) {
					sig = false;
					pool.forEach(function(k,i){
						if(o.source === k || o.target === k) 
							sig = true;
					});
					return sig === true? marker(color(o.Group_2D), 1.0) : marker(color(o.Group_2D), 0.05);
				});
				break;
			default:
				link.attr("marker-end", function(o) {
					sig = false;
					pool.forEach(function(k,i){
						if(o.source === k || o.target === k) 
							sig = true;
					});
					return sig === true? marker(color(o.Gephi), 1.0) : marker(color(o.Gephi), 0.05);
				});
				break;
		}
		
		pool.forEach(function(k,i){
			if(k.id == main_node.id){
				var table = d3.select("#node_info");

			// add in data
				table.select("#id").select("td").text(k.id);
				table.select("#group").select("td").text(k.Gephi);
				table.select("#inLinks").select("td").text( (k.in_size - 2) / .5);
				table.select("#outLinks").select("td").text( (k.out_size - 2) / .5);
			}
			
		});
		
		node.attr("r",  function(k) {
			var child_name = '.' + main_node.id.replace('|','.');
			if(child_name[ child_name.length-1 ] == '.')
				child_name = child_name.slice(0,-1);
			var idx = k.id.lastIndexOf(child_name);
			if (k.id == main_node.id)
				return 7.;
			else if( idx > 0 ){
				var node;
				pool.forEach(function(d){
					if(d.id === k.id)
						node = d;
				});
				if(node){
					var tmp = k.id.slice(0,idx);
					return 7.0 - tmp.replace('|','.').split('.').length;
				}
			}
			else
				return 4;
		});
		
		if(flag===true){
			var p = name2path(d.id);
			if(p){
				flag=false;
				click2(p);
				mouseover(p);
				click3(d.id);
				flag=true;
			}
		}
			
}
function name2path(name){
	var node_name = name;
	if(node_name[node_name.length-1] == '|')
		node_name = node_name.slice(0,-1);
	var arr = node_name.replace('|','.').split('.');
	console.log(arr);
	var i = arr.length-1;
	var p;
	path.attr('id',function(d){
		var j;
		if( d.data.name != "root") return "sunpath";
		p = d;
		while( i>=0 ){
			var children = p.children;
			if(!p.children) break;
			var sig = false;
			for(j = 0; j<children.length; j++){
				if( children[j].data.name == arr[i] ){
					sig = true;
					p = children[j];
				}
			}
			if( sig === false ) break;
			console.log(i+ " : " +arr[i]);
			i-=1;
		}
		return "sunpath";
	});
	if(i<0)
		return p;
	else
		return null;
}
function isConnected(a, b) {
    return linkedByIndex[a.index + "," + b.index] || linkedByIndex[b.index + "," + a.index] || a.index == b.index;
}
function marker(color, opacity) {

        defs.append("svg:marker")
            .attr("id", color.replace("#", "") + opacity)
            .attr("viewBox", "0 -5 10 10")
            .attr("refX", 15) // This sets how far back it sits, kinda
            .attr("refY", 0)
            .attr("markerWidth", 6)
            .attr("markerHeight", 6)
            .attr("orient", "auto")
			.attr("fill-opacity", opacity)
			.attr("stroke-opacity", opacity)
            .attr("markerUnits", "userSpaceOnUse")
            .append("svg:path")
            .attr("d", "M0,-5L10,0L0,5")
            .style("fill", color);
        
        return "url(" + color + opacity + ")";
}

function makeForceDirected(){

//Define where to look for nodes and where to look for links
const NODE_FILE =  "csv_files/fdd_nodes.csv"
const LINK_FILE = "csv_files/fdd_links.csv"

//Load up pre-defined svg

var	width = +svg.attr("width"),
	height = +svg.attr("height");

// add forces
var simulation = d3.forceSimulation()
	.force("link", d3.forceLink().id(function(d) {return d.id; })
								 .strength(link => link.value)
								 .distance(link => 1.0/link.value))
	.force("charge", d3.forceManyBody().strength(-40))
	//.force("picky centre", pickyForce)
	.force("collide", d3.forceCollide().radius(6))
	.force("center", d3.forceCenter(width , height/0.95));




//Open up node data file 
d3.csv(NODE_FILE, function(nodes_data) {

	//Create empty graph array
	graph = { "links": [] , "nodes": []};

	//Push in node data (both ID and class) from nodepath
	nodes_data.forEach(node => graph.nodes.push( { "id":node.sequence , "Gephi":node.node2vec128D, "Group_15D":node.struc2vec128D, "Group_2D":node.struc2vec2D, "in_size":1., "out_size":1.} ) );

	//Open up the links file, and push link data in too
	d3.csv(LINK_FILE, function(links_data) {
		links_data.forEach(link => graph.links.push( link ) );

	//create a "size" argument on the graph.nodes variables
		var i;
		for (i = 0; i < graph.nodes.length; i++) {
			for (j =0; j < graph.links.length; j++) {
				if (graph.nodes[i].id === graph.links[j].source) {
					graph.nodes[i].out_size += 0.3
					graph.links[j].Gephi = graph.nodes[i].Gephi
					graph.links[j].Group_15D = graph.nodes[i].Group_15D
					graph.links[j].Group_2D = graph.nodes[i].Group_2D
			}; 
				if (graph.nodes[i].id === graph.links[j].target) {
					graph.nodes[i].in_size += 0.3
			};
			};
			};



	//Create the link and node elements visually.
 		link = svg.append("g")
      		.attr("class", "links")
    		.selectAll("line")
    		.data(graph.links)
    		.enter().append("line")
      		//.attr("stroke-opacity", function(d) { return (d.value); })
			//.attr('marker-end','url(#arrowhead)').attr("stroke-opacity", function(d) { return (d.value); });
			.each(function(d) {
            var colour = color(d.Gephi);
			var opacity = d.value;
            d3.select(this).attr("stroke-opacity", opacity)
                           .attr("marker-end", marker(colour, opacity));
        });

  		node = svg.append("g")
      		.attr("class", "nodes")
    		.selectAll("circle")
    		.data(graph.nodes)
    		.enter().append("circle")
      		.attr("r",  function(d) { return 4; } )
			.attr("fill", function(d) { return color(d.Gephi); });


     		//.on("mouseover", mouseOver(.2))
      		//.on("mouseout", mouseOut)
			node.on("click" , function(d){
				save.length = 0;
				pool.push(d);
				main_node=d;
				click1(d);
				pool.length=0;
			})
			.on("mouseover",function(d){
				if(clicked === true){
					node.style("fill-opacity", function(o) {
						sig = false;
						save.forEach(function(k,i){
							if(isConnected(k, o)) 
								sig = true;
						});
						if(o === d)
							sig = true;
						return sig === true? 1: 0.05;
					});
				}
			})
			.on("mouseout",function(d){
				if(clicked === true){
					node.style("fill-opacity", function(o) {
						sig = false;
						save.forEach(function(k,i){
							if(isConnected(k, o)) 
								sig = true;
						});
						return sig === true? 1: 0.05;
					});
				}
			})
			.call(d3.drag()
          		.on("start", dragstarted)
          		.on("drag", dragged)
          		.on("end", dragended));

		// double click anywhere on svg  to un-highlight
		svg.on("dblclick" , function(d){
			clicked = false;
			node.style("stroke-opacity", 1);
        	node.style("fill-opacity", 1);
			node.attr("r", 4);
        	link.style("stroke-opacity", function(c) { return (c.value); });
        	link.style("stroke", "gray");

			switch(Grouping) {
				case "Gephi":
      				link.attr("marker-end", function(o) {
					return marker(color(o.Gephi), 1.0);
           		});
					break;
				case "D15":
					link.attr("marker-end", function(o) {
					return marker(color(o.Group_15D), 1.0);
           		});
					break;
				case "D2":
					link.attr("marker-end", function(o) {
					return marker(color(o.Group_2D), 1.0);
           		});
					break;
				default:
					link.attr("marker-end", function(o) {
					return marker(color(o.Gephi), 1.0);
           		});
					break;
			}


		});

  node.append("title")
      .text(function(d) { return d.id; });

  simulation
      .nodes(graph.nodes)
      .on("tick", ticked);

  simulation.force("link")
      .links(graph.links);

  function ticked() {
    link
        .attr("x1", function(d) { return d.source.x/1.98; })
        .attr("y1", function(d) { return d.source.y/1.98;})
        .attr("x2", function(d) { return d.target.x/1.98; })
        .attr("y2", function(d) { return d.target.y/1.98; });

    node
        .attr("cx", function(d) { return d.x/1.98; })
        .attr("cy", function(d) { return d.y/1.98; });
  }


//~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~//
//Trying to add hover network info

    graph.links.forEach(function(d) {
        linkedByIndex[d.source.index + "," + d.target.index] = 1;
    });

    // check the dictionary to see if nodes are linked


d3.selectAll("input[name=filter]").on("change", function(d){

  // value of selected radio
  var value = this.value;

	switch (value) {
		case "none":
			node.attr("r",  function(d) { return 4;} )
			break;
		case "all":
			node.attr("r",  function(d) { return Math.min(d.out_size + d.in_size, 40.0); } )
			break;
		case "in":
			node.attr("r",  function(d) { return Math.min(d.in_size, 40.0); } )
			break;
		case "out":
			node.attr("r",  function(d) { return Math.min(d.out_size, 40.0);} )
			break;
		default:
			node.attr("r",  function(d) { return 4;} )
	}


});


d3.selectAll("input[name=grouping]").on("change", function(d){

  // value of selected grouping
  var value = this.value;

	switch (value) {
		case "gephi":
			Grouping = "Gephi"
			switch(clicked) {
				case true:
					link.attr("marker-end", function(o) {
					return o.source === d || o.target === d ? marker(color(o.Gephi), 1.0) : 
						marker(color(o.Gephi), 0.1);
				});
				break;
				case false:
					link.attr("marker-end", function(d) {return marker(color(d.Gephi), d.value)})
				break;
				default: 
					link.attr("marker-end", function(d) {return marker(color(d.Gephi), d.value)})
				}
			node.attr("fill", function(d) { return color(d.Gephi); });
			break;

		case "D15":
			Grouping = "D15"
			switch(clicked) {
				case true:
					link.attr("marker-end", function(o) {
					return o.source === d || o.target === d ? marker(color(o.Group_15D), 1.0) : 
						marker(color(o.Gephi), 0.1);
				});
				break;
				case false:
					link.attr("marker-end", function(d) {return marker(color(d.Group_15D), d.value)})
				break;
				default: 
					link.attr("marker-end", function(d) {return marker(color(d.Group_15D), d.value)})
				}
			node.attr("fill", function(d) { return color(d.Group_15D); });		
			break;

		case "D2":
			Grouping = "D2"
			switch(clicked) {
				case true:
					link.attr("marker-end", function(o) {
					return o.source === d || o.target === d ? marker(color(o.Group_2D), 1.0) : 
						marker(color(o.Gephi), 0.1);
				});
				break;
				case false:
					link.attr("marker-end", function(d) {return marker(color(d.Group_2D), d.value)})
				break;
				default: 
					link.attr("marker-end", function(d) {return marker(color(d.Group_2D), d.value)})
				}
			node.attr("fill", function(d) { return color(d.Group_2D); });
			break;
		default:
			link.attr("marker-end", function(d) {return marker(color(d.Gephi), d.value)})
			link.style("stroke", function(d) {return color(d.Gephi)})
			node.attr("fill", function(d) { return color(d.Gephi); })
	}


});


	});//close links file
});//close nodes file


function dragstarted(d) {
  if (!d3.event.active) simulation.alphaTarget(0.3).restart();
  d.fx = d.x;
  d.fy = d.y;
}

function dragged(d) {
  d.fx = d3.event.x;
  d.fy = d3.event.y;
}

function dragended(d) {
  if (!d3.event.active) simulation.alphaTarget(0);
  d.fx = null;
  d.fy = null;
}

} // end main function

makeForceDirected();
//----------------------------------------------------------------------------------------------------------------------------------------------//
//----------------------------------------------------------------------------------------------------------------------------------------------//

