/* make an episogram
 * 
 * a line of nodes colored by url
 * arc surrounding node indicates duration
 * 
 */

function makeEpisogram(){

// constants
const INPUT_FILE = "json_files/episogram_data_mini.json";
const INPUT_WEEKS = "json_files/assignments_by_week.json"
const SPACING = 50;
const BASE_Y = 400;
const NODE_RAD = 12;
const WEEK_HEIGHT = 200; /* WEEK_HEIGHT must be less than BASE_Y */

//~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
// creates the line of sequence given a sequence data array
// returns a the nodes of the line for click/mouseover usage
function createSequenceLine( svg , sequence ){
	
	// add a horizontal line for nodes to lie on
	var baseline = svg
		.append("line")
			.attr("class" , "base_line")
			.attr("x1" , SPACING  )
			.attr("x2" , sequence.length * SPACING) 
			.attr("y1" , BASE_Y )
			.attr("y2" , BASE_Y )
			.attr("stroke" , "blue")
			.attr("stroke-width" , "2");

	// add circles to indicate where the next node in sequence
	var epis_nodes = svg.selectAll( "circle" )
		.data( sequence ).enter()
		.append("circle")
			.attr("class" , "seq_node")
			.attr("cx" , node => sequence.indexOf(node) * SPACING + SPACING)
			.attr("cy" , BASE_Y)
			.attr("r" , NODE_RAD)
			.attr("fill" , "red")
		.append("title")
        	.text(function(d, i) { return "Node: " + d; });

	// add arcs for each node to display duration
	sequence.forEach( function(end_angle , index) {
		var arc = d3.arc()
			.innerRadius(NODE_RAD + 1)
			.outerRadius(NODE_RAD + 3)
			.startAngle(3) //converting from degs to radians
			.endAngle( parseInt(end_angle) * (Math.PI/180)); //just radians

		svg.append("path")
			.attr("d", arc)
			.attr("transform", function(node){
				return "translate(" + (index * SPACING + SPACING) + "," + BASE_Y + ")";
			});
	});

	// return the nodes
	return epis_nodes;

}


//~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
function main(){

	// create an svg element
	var width = 600,
		height = 600;

	var epis_svg = d3.select("#episogram").append("svg")
    	.attr("width", width)
    	.attr("height", height)

	var test_seq = [ "34" , "17" , "25" , "27" , "84" ];

	createSequenceLine( epis_svg , test_seq );

}

main();



} // closes makeEpisogram()
makeEpisogram();
