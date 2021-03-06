
//----------------------------------------------------------------------------------------------------------------------------------------------//
//----------------------------------------------------------------------------------------------------------------------------------------------//
//console.log(node);
var pool = new Array();
var width = 330,
    height = 330,
	radius = (Math.min(width, height) / 2) - 10;
var x = d3.scaleLinear()
    .range([0, 2 * Math.PI]);

var y = d3.scaleSqrt()
    .range([0, radius]);

//var color2 = d3.scaleOrdinal(d3.schemeCategory20c);
var color2 = d3.scaleOrdinal()
      .domain(['29','0','1','34','2','3','7','9','10','11','14','19','22','24','25','26','21','28','30','5','31',     '4','6','8','12','15','16','17','20','13','23','27','32','33',         '36','37',      '18'])
      .range([ "#56b4e9","#56b4e9","#56b4e9","#56b4e9","#56b4e9","#56b4e9","#56b4e9","#56b4e9","#56b4e9","#56b4e9","#56b4e9","#56b4e9","#56b4e9","#56b4e9","#56b4e9","#56b4e9","#56b4e9","#56b4e9","#56b4e9","#56b4e9","#56b4e9", "#0072b2","#0072b2","#0072b2","#0072b2","#0072b2","#0072b2","#0072b2","#0072b2","#0072b2","#0072b2","#0072b2","#0072b2","#0072b2",                   "#e69f00","#e69f00",              "#d55e00" ]);
var partition = d3.partition();
var svg2 = d3.select("#sunburst_diagram").append("svg")
    .attr("width", width)
    .attr("height", height)
    .append("g")
    .attr("transform", "translate(" + width / 2 + "," + (height / 2) + ")");
var arc = d3.arc()
    .startAngle(function(d) { return Math.max(0, Math.min(2 * Math.PI, x(d.x0))); })
    .endAngle(function(d) { return Math.max(0, Math.min(2 * Math.PI, x(d.x1))); })
    .innerRadius(function(d) { return Math.max(0, y(d.y0)); })
    .outerRadius(function(d) { return Math.max(0, y(d.y1)); });
var path;
function click2(d) {
	// zoom in feature
	svg2.transition()
		.duration(750)
      	.tween("scale", function() {
			var xd = d3.interpolate(x.domain(), [d.x0, d.x1]),
    			yd = d3.interpolate(y.domain(), [d.y0, 1]),
        		yr = d3.interpolate(y.range(), [d.y0 ? 20 : 0, radius]);
        	return function(t) { x.domain(xd(t)); y.domain(yd(t)).range(yr(t)); };
      	})
    	.selectAll("path")
      	.attrTween("d", function(d) { return function() { 
				return arc(d); 
		}; });
	if(d.data.name === "root") { dbclick();return; }
	//~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	// clear data table
	d3.select("#scrollable-content").select("table").select("tbody").selectAll("tr").remove();
	
	// fill in data table
	
	// display name of sequence
	var name_seq = "";

	var tmp_node = d;
	while(tmp_node.parent){
		name_seq = tmp_node.data.name + "-" + name_seq;
		tmp_node = tmp_node.parent;
	}
	if(name_seq[ name_seq.length - 1 ] === "-")
		name_seq = name_seq.slice(0, -1);

	document.getElementById("node_sequence").innerHTML = name_seq;
	if(flag===true){
	//construct the name of the node
	var n = d;
	var node_name = n.data.name + "|";
	var child_name = n.data.name + ".";
	while(n.parent){
		n = n.parent;
		node_name = node_name + n.data.name + ".";
		child_name = child_name + n.data.name + ".";
	}
	child_name = child_name.slice(0, -6);
	
	if(node_name[ node_name.length - 6 ] === ".")
		node_name = node_name.slice(0, -6);
	else
		node_name = node_name.slice(0, -5);
	
		node.attr("r",  function(d){ 
			if(d.id == node_name){
				main_node = d;
				console.log(d.id);
				pool.push(d);
			}
			else if(d.id.endsWith(child_name)){
				console.log(d.id);
				pool.push(d);
			}
			return 5.; 
		});
		flag = false;
		save.length = 0;
		click1(pool[0]);
		pool.length=0;
		click3(node_name);
		flag = true;
	}
	// use the sequence name to find matches
	// then display in scrollable content
	d3.csv("csv_files/sequence.csv" , function(input){
		var matching = [];

		// add the matching people to the array
		input.forEach( function(object,i){

			var seq_indices = getIndicesOf(name_seq , object.sequence);

			if( seq_indices.length > 0 ){
				newObj = object;
				newObj.num_seq = seq_indices.length;
				newObj.no = i+1;
				seq_indices.forEach( function(i){
					newObj.sequence = newObj.sequence.replaceAll( name_seq , '...' )
				});
				matching.push(newObj);
			}
		});
		matching.sort(function(a,b){ return a.num_seq > b.num_seq?false:true; });
		// display data in scrolllable table		
 		var rows = d3.select("#scrollable-content").select("table").select("tbody").selectAll("tr")
			.data(matching, function (d) {return d;});

		rows.enter()
			.append('tr')
			.selectAll("td")
			.data(function (d) {return [d.no.toString(),d.num_seq, d.sequence];})
			.enter()
			.append("td")
			.text(function(d) { return d; });

		rows.exit().remove();

		var cells = rows.selectAll('td')
			.data(function (d) {return [d.no.toString(),d.num_seq, d.sequence];})
			.text(function (d) {return d;});

		cells.enter()
			.append("td")
			.text(function(d) { return d; });

		cells.exit().remove();
	});
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
var sequence = 	d3.select("#active_sequence").append("svg")
	.attr("width" , 400)
	.attr("height" , 50);
	
function mouseover(d) {
	d3.selectAll("#active_sequence_data").remove();
	// display on screen the current sequence
	var node = d;
	while(node.parent){
		// add rectangles
		sequence.append("rect")
			.attr("id" , "active_sequence_data")
			.attr("width" , 50)
			.attr("height" , 30)
			.style("fill", function(e) { return color2(node.data.name); })
			.attr("transform" , function(e){ return "translate(" + (node.depth * 50 - 50) + ", 0)"})
		// add text
		sequence.append("text")
			.attr("id" , "active_sequence_data")
    		.attr("x", function(e) { return node.depth * 50 - 25; })
    		.attr("y", 20)
    		.attr("dy", ".35em")
    		.text(function(e) { return node.data.name; });
		
		node = node.parent;
	}
	
}
function makeSunburst(){

const INPUT_FILE = "json_files/sunburst_data_struc2vec.json"

// center pie chart
var pieChart = d3.pie().value(function(d) { return 5; });



// add svg element

// load in data
d3.json(INPUT_FILE, function(error, root) {
  
  if (error) throw error;
  
  root = d3.hierarchy(root);

  root.sum(function(d) { return d.size; });
  path = svg2.selectAll("path")
      .data(partition(root).descendants())
      .enter().append("path")
	  .attr("id" , "sun_path")
      .attr("d", arc )
      .style("fill", function(d) { return color2(d.data.name); })
      .on("click", click2)
	  .on("mouseover" , mouseover)
      .append("title")
      .text(function(d) { return "name: " + d.data.name + "\n" + d.value.toString() + " times"; });
});



String.prototype.replaceAll = function(str1, str2, ignore) 
{
    return this.replace(new RegExp(str1.replace(/([\/\,\!\\\^\$\{\}\[\]\(\)\.\*\+\?\|\<\>\-\&])/g,"\\$&"),(ignore?"gi":"g")),(typeof(str2)=="string")?str2.replace(/\$/g,"$$$$"):str2);
} 
url_file = "csv_files/object_ref_type.csv";
d3.csv(url_file,function(error,data){
	data.sort(function(a, b) { return a.num - b.num; });
	d3.select("#url_table").style.background = "blue";
	d3.select("#url_table").select("table").select("tbody")
		.selectAll("tr")
		.data(data)
		.enter()
		.append("tr")
		.selectAll("td")
		.data(function(d){ return [d.num,d.url,d.type,d.week]; })
		.enter()
		.append("td")
		.text(function(d){ return d; });
	
});

} // end scope for webpage

makeSunburst();
