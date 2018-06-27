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

//Define where to look for nodes and where to look for links
var nodepath = "nodes_doubly_classified.csv"
var linkpath = "weights-network-cell.csv"

//Load up pre-defined svg
var svg = d3.select("#hon_diagram").select("svg"),
	/*.call(d3.zoom().on("zoom", function () {
        svg.attr("transform", d3.event.transform)
})),*/
	width = +svg.attr("width"),
	height = +svg.attr("height");


var defs = svg.append("svg:defs");

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
    };

var color = d3.scaleOrdinal(d3.schemeCategory20);

/*
// Custom implementation of a force applied to only every second node
var pickyForce = d3.forceManyBody().strength(-50);

// Save the default initialization method
var init = pickyForce.initialize; 

// Custom implementation of .initialize() calling the saved method with only
// a subset of nodes
pickyForce.initialize = function(nodes) {
    // Filter subset of nodes and delegate to saved initialization.
    init(nodes.filter(function(n) { return (+n.group != "12"); }));
    };
*/


var simulation = d3.forceSimulation()
	.force("link", d3.forceLink().id(function(d) {return d.id; })
								 .strength(link => link.value)
								 .distance(link => 1./link.value))
	.force("charge", d3.forceManyBody().strength(-10))
	//.force("picky centre", pickyForce)
	.force("collide", d3.forceCollide().radius(6))
	.force("center", d3.forceCenter(width / 2, height / 2));




//Open up node data file function(d) { console.log(d.value); return (d.value); }
d3.csv(nodepath, function(nodes_data) {
	//Create empty graph array
	graph = { "links": [] , "nodes": []};

	//Push in node data (both ID and class) from nodepath
	nodes_data.forEach(node => graph.nodes.push( { "id":node.sequence , "Gephi":node.Gephi, "Group_15D":node.KMeans_15D, "Group_2D":node.KMeans_2D, "in_size":2., "out_size":2.} ) );

	//Open up the links file, and push link data in too
	d3.csv(linkpath, function(links_data) {
		links_data.forEach(link => graph.links.push( link ) );

	//create a "size" argument on the graph.nodes variables
		var i;
		for (i = 0; i < graph.nodes.length; i++) {
			for (j =0; j < graph.links.length; j++) {
				if (graph.nodes[i].id === graph.links[j].source) {
					graph.nodes[i].out_size += 0.5
					graph.links[j].Gephi = graph.nodes[i].Gephi
			}; 
				if (graph.nodes[i].id === graph.links[j].target) {
					graph.nodes[i].in_size += 0.5
			};
			};
			};



	//Create the link and node elements visually.
 		var link = svg.append("g")
      		.attr("class", "links")
    		.selectAll("line")
    		.data(graph.links)
    		.enter().append("line")
      		//.attr("stroke-opacity", function(d) { return (d.value); })
			//.attr('marker-end','url(#arrowhead)').attr("stroke-opacity", function(d) { return (d.value); });
			.each(function(d) {
            var colour = color(d.Gephi);
			var opacity = d.value;
            d3.select(this).style("stroke", colour)
						   .attr("stroke-opacity", opacity)
                           .attr("marker-end", marker(colour, opacity));
        });

		var clicked = false;

  		var node = svg.append("g")
			.attr("id" , "fdd_g")
      		.attr("class", "nodes")
    		.selectAll("circle")
    		.data(graph.nodes)
    		.enter().append("circle")
      		.attr("r",  function(d) { return 5.; } )
      		.attr("fill", function(d) { return color(d.Gephi); })
     		//.on("mouseover", mouseOver(.2))
      		//.on("mouseout", mouseOut)
			.on("click" , function(d){

				/* highlight travel path for nodes */

				// check all other nodes to see if they're connected
            	// to this one. if so, keep the opacity at 1, otherwise
            	// fade
            	node.style("stroke-opacity", function(o) {
                	thisOpacity = isConnected(d, o) ? 1 : 0.1;
                	return thisOpacity;
            	});
            	node.style("fill-opacity", function(o) {
                	thisOpacity = isConnected(d, o) ? 1 : 0.1;
                	return thisOpacity;
            	});
            	// also style link accordingly
            	link.style("stroke-opacity", function(o) {
                	return o.source === d || o.target === d ? 1 : 0.1;
				});
				link.attr("marker-end", function(o) {
					return o.source === d || o.target === d ? marker(color(o.Gephi), 1.0) : 
						marker(color(o.Gephi), 0.1);
           		});


				let table = d3.select("#node_info");

				// add in data
				table.select("#id").select("td").text(d.id);
				table.select("#group").select("td").text(d.Gephi);
				table.select("#inLinks").select("td").text( (d.in_size - 2) / .5);
				table.select("#outLinks").select("td").text( (d.out_size - 2) / .5);
			})
			.call(d3.drag()
          		.on("start", dragstarted)
          		.on("drag", dragged)
          		.on("end", dragended));

			
		// double click anywhere on svg to un-highlight
		svg.on("dblclick" , function(d){
			node.style("stroke-opacity", 1);
        	node.style("fill-opacity", 1);
        	link.style("stroke-opacity", function(d) { return (d.value); });
        	link.style("stroke", "#999");
			link.each(function(d) {
       			var colour = color(d.Gephi);
				var opacity = d.value;
       			d3.select(this).style("stroke", colour)
				   .attr("stroke-opacity", opacity)
                   .attr("marker-end", marker(colour, opacity));
			});
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
        .attr("x1", function(d) { return d.source.x; })
        .attr("y1", function(d) { return d.source.y; })
        .attr("x2", function(d) { return d.target.x; })
        .attr("y2", function(d) { return d.target.y; });

    node
        .attr("cx", function(d) { return d.x; })
        .attr("cy", function(d) { return d.y; });
  }


//~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~//
//Trying to add hover network info
var linkedByIndex = {};
    graph.links.forEach(function(d) {
        linkedByIndex[d.source.index + "," + d.target.index] = 1;
    });

    // check the dictionary to see if nodes are linked
    function isConnected(a, b) {
        return linkedByIndex[a.index + "," + b.index] || linkedByIndex[b.index + "," + a.index] || a.index == b.index;
    }

    /*// fade nodes on hover
    function mouseOver(opacity) {
		console.log("mouseover");
        return function(d) {
            // check all other nodes to see if they're connected
            // to this one. if so, keep the opacity at 1, otherwise
            // fade
            node.style("stroke-opacity", function(o) {
                thisOpacity = isConnected(d, o) ? 1 : 0.1;
                return thisOpacity;
            });
            node.style("fill-opacity", function(o) {
                thisOpacity = isConnected(d, o) ? 1 : 0.1;
                return thisOpacity;
            });
            // also style link accordingly
            link.style("stroke-opacity", function(o) {
                return o.source === d || o.target === d ? 1 : 0.1;
			});

			link.attr("marker-end", function(o) {
				return o.source === d || o.target === d ? marker(color(o.group), 1.0) : marker(color(o.group), 0.1);
            });
        };
    }

    function mouseOut() {
        node.style("stroke-opacity", 1);
        node.style("fill-opacity", 1);
        link.style("stroke-opacity", function(d) { return (d.value); });
        link.style("stroke", "#999");
		link.each(function(d) {
            var colour = color(d.group);
			var opacity = d.value;
            d3.select(this).style("stroke", colour)
						   .attr("stroke-opacity", opacity)
                           .attr("marker-end", marker(colour, opacity));
        });
    }*/



d3.selectAll("input[name=filter]").on("change", function(d){

  // value of selected radio
  var value = this.value;

	switch (value) {
		case "none":
			node.attr("r",  function(d) { return 5.} )
			break;
		case "all":
			node.attr("r",  function(d) { return d.out_size + d.in_size; } )
			break;
		case "in":
			node.attr("r",  function(d) { return d.in_size; } )
			break;
		case "out":
			node.attr("r",  function(d) { return d.out_size;} )
			break;
		default:
			node.attr("r",  function(d) { return 5.} )
	}


});




d3.selectAll("input[name=grouping]").on("change", function(d){

  // value of selected grouping
  var value = this.value;

	switch (value) {
		case "gephi":
			link.attr("marker-end", function(d) {return marker(color(d.Gephi), d.value)})
			link.style("stroke", function(d) {return color(d.Gephi)})
			node.attr("fill", function(d) { return color(d.Gephi); })
			break;
		case "D15":
			link.attr("marker-end", function(d) {return marker(color(d.Group_15D), d.value)})
			link.style("stroke", function(d) {return color(d.Group_15D)})
			node.attr("fill", function(d) { return color(d.Group_15D); })			
			break;
		case "D2":
			link.attr("marker-end", function(d) {return marker(color(d.Group_2D), d.value)})
			link.style("stroke", function(d) {return color(d.Group_2D)})
			node.attr("fill", function(d) { return color(d.Group_2D); })	
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


