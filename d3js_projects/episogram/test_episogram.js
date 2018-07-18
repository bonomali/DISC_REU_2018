/* make an episogram
 * 
 * a line of nodes colored by url
 * arc surrounding node indicates duration
 * 
 */

function makeEpisogram(){

/*************************************************************************
 * Graph Layout
 *			   								  _
 *			   						|------->|_| grade distribution sankey
 *			node name				|--/	 |_|
 *			   |	  		   		|----\	 |_|
 *			   |	  		   		|------->|_|
 *	sequence---*------*--------*--->|--/     |_|
 *
 *************************************************************************/

// constants
const INPUT_FILE = "json_files/episogram_data_mini.json";
const INPUT_WEEKS = "json_files/assignments_by_week.json"
const SPACING = 50;
const BASE_Y = 400;
const NODE_RAD = 7;
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


	var arc = d3.arc()
		.innerRadius(NODE_RAD + 1)
		.outerRadius(NODE_RAD + 3)
		.startAngle(3) //converting from degs to radians
		.endAngle( 45 * (Math.PI/180)); //just radians
	
	var duration_arcs = svg.selectAll("path")
		.data(sequence).enter()
		.append("path")
			.attr("d", arc)
			.attr("transform", function(node){
				return "translate(" + (sequence.indexOf(node) * SPACING + SPACING) + "," + BASE_Y + ")";
			})


	// return the nodes
	return epis_nodes;

}


//~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
// creates the main semester line given the data object
// returns a the nodes of the line for click/mouseover usage
function createBaseLine( svg , data ){

	// get an array of weeks in the semester
	var weeks = weeksInSemester(data);
	
	// add a horizontal line ( should be lower on the svg so data will fit )
	svg.append("line")
		.attr("class" , "base_line")
		.attr("x1" , SPACING  )
		.attr("x2" , weeks.length * SPACING + SPACING) 
		.attr("y1" , BASE_Y )
		.attr("y2" , BASE_Y )
		.attr("stroke" , "blue")
		.attr("stroke-width" , "2");
	
	// add circles to indicate where the weeks should be
	var epis_nodes = svg.selectAll( "base_node" )
		.data( weeks ).enter()
		.append("circle")
		.attr("class" , "base_node")
		.attr("cx" , week => week * SPACING + SPACING)
		.attr("cy" , BASE_Y)
		.attr("r" , BASE_NODE_RAD)
		.attr("fill" , "red");
  
	
	// return the nodes
	return epis_nodes;

}

//~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
// find the number of weeks in the semester given the data object
// returns an array from 1 to number of weeks
function weeksInSemester( data ) {

	num_weeks = -1;
	
	// loop through all data and find max num of weeks
	Object.keys(data).forEach( function( student ){
		data[student].forEach( function( assignment ){
			
			assign_week = parseInt( assignment.week , 10 ); // string to int
			if( assign_week > num_weeks)
				num_weeks = assign_week;

		});
	});

	// create an array of weeks
	weeks = [];
	for( var i = 1; i <= num_weeks; i++ )
		weeks.push(i);

	return weeks;
}

//~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
function updateTableAssigns( weekObj ){
	
	const NAME = 4;

	// clear list
	d3.selectAll(".assign_node").remove();

	// search for unique assigns in weekObj
	var assigns = weekObj[ Object.keys( weekObj )[0] ];
	var uniqueAssigns = []

	assigns.forEach( function(assign){
		var foundUnique = true;

		if(uniqueAssigns.length === 0)
			uniqueAssigns.push(assign[NAME]);

		if(assign[NAME] in uniqueAssigns){
			foundUnique = false;
		}

		if(foundUnique)
			uniqueAssigns.push(assign[NAME]);

	});

	// add an unordered list of assigns
	d3.select("#assigns_list")
		.data( uniqueAssigns )
		.enter()
		.append( "ul" )
		.attr("class" , "assign_node")
		.text( name => name );

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

	/*

	// data loaded in should be an object of students
	// students are arrays of assignment objects
	d3.json(INPUT_FILE , function(assignsByStudent){

		// create a baseline (rewrite w/ assignsByWeek)
		var baseLine = createBaseLine( epis_svg , assignsByStudent );
	
		// get the data formatted by week (python?)
		// ie assignmentsByWeek = [ { week : [ assign ] } , ... ]
		d3.json(INPUT_WEEKS , function(assignsByWeek){
			
			
			// add hover data to base week node
			baseLine.on("click" , function(week_num){
			
				/* display summary of week data
				 * including:
				 *	unique assignments names
				 *	number of people that attempted them
				 *

				// clear data table
				d3.selectAll(".epis_table").text("");
				
				// fill in html table
				d3.select("#table_week").text(week_num);

				// get correct week data
				assignsByWeek.forEach(function(week){
					if( week_num == Object.keys(week)[0] ){
							
						// add main assignments
						updateTableAssigns(week);

					}
				});
			});
	

			// add nodes for each assignment
			//
			//
			// add click/mouseover functionality to assignments
			//
			//

		});


	});

	*/

}

main();



} // closes makeEpisogram()

makeEpisogram();
