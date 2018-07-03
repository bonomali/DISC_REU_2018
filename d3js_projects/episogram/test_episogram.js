/* make an episogram
 * 
 * uses a semester line of weeks
 * each week has 7 days
 * 
 * display the assignements done on that day
 *
 *
 */

/*************************************************************************
 * Necessary fxns:
 * 		addHorizLine( className , arrayOfinfo )
 * 			- creates a horizontal line of a certain class using array
 *
 * 		addVertiLine( className , arrayOfInfo )
 * 			- creates a vertical line of a certain class using array
 *
 * 	Need an array of order of class names
 *************************************************************************/

//~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
function addHorizLine( svg , className , data , x = 0 , y = 0 ){

	// define class names
	var lineClass = className + "_line";
	var nodeClass = className + "_node";

	// add horiz line
	svg.append("line")
		.attr("class" , lineClass)
		.attr("x1" , x * 25)
		.attr("x2" , x * 25 + 500)
		.attr("y1" , y * 25 + 10)
		.attr("y2" , y * 25 + 10)
		.attr("stroke" , "blue")
		.attr("stroke-width" , "2")

	// add nodes
	var epis_nodes = svg.selectAll( nodeClass )
		.data( data ).enter()
		.append("circle")
		.attr("class" , nodeClass)
		.attr("cx" , d => d * 25 + (x * 25) )
		.attr("cy" , y * 25 + 10)
		.attr("r" , 10)
		.attr("fill" , "red");

	return epis_nodes
}

//~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
function addVertiLine( svg , className , data , x = 0 , y = 10 ){

	// define class names
	var lineClass = className + "_line";
	var nodeClass = className + "_node";

	// add verti line
	svg.append("line")
		.attr("class" , lineClass)
		.attr("x1" , x * 25 - 10)
		.attr("x2" , x * 25 - 10)
		.attr("y1" , y)
		.attr("y2" , y + 200)
		.attr("stroke" , "blue")
		.attr("stroke-width" , "2")

	// add nodes
	var epis_nodes = svg.selectAll( nodeClass )
		.data( data ).enter()
		.append("circle")
		.attr("class" , nodeClass)
		.attr("cx" , x * 25 - 10)
		.attr("cy" , d => d * 25 + y )
		.attr("r" , 10)
		.attr("fill" , "red");

	return epis_nodes
}

//~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
// find the number of weeks in the semester given the data object
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

function daysInWeek( data ){

	return [ 1 , 2 , 3 , 4 , 5 , 6 , 7 ];

}

function fillTable( data ){
	// fill in data table
	d3.select("#table_date").text("");
	d3.select("#table_week").text(data);

}

/*
//~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
// when a week node is clicked, a week line should be created with 7 day nodes
function clickWeekNode( week , data , svg ){

	// clear old lines
	clearLines();

	// fill in data table
	d3.select("#table_date").text("");
	d3.select("#table_week").text(week);

	// add week line going downward
	svg.append("line")
		.attr("class" , "week_line")
		.attr("x1" , week * 25 - 10)
		.attr("x2" , week * 25 - 10)
		.attr("y1" , 50)
		.attr("y2" , 50)
		.attr("stroke" , "blue")
		.attr("stroke-width" , "2")
		.transition()
		.attr("y2" , 7 * 50 + 50)

	// layering
	

	// make an array of seven days
	days = [1 , 2, 3, 4, 5, 6, 7];

	// add day nodes
	var day_nodes = svg.selectAll(".day_node")
		.data( days ).enter()
		.append("circle")
		.attr("class" , "day_node")
		.attr("cx" , week * 25 - 10)
		.attr("cy" , day => day * 50 + 50)
		.attr("r" , 0)
		.attr("fill" , "red")
		.on("click" , day => clickDayNode( day , data , svg ) )
		.transition()
		.attr("r" , 10);
		
	return day_nodes
}

function clickDayNode( day , data , svg ){

	// fill in data table
	d3.select("#table_date").text(day);
}
*/

function clearLines( className ){
	d3.selectAll("." + className + "_node")
		.remove();

	d3.selectAll("." + className + "_line")
		.remove();
}

//~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
function main(){

	// variables and constants
	const INPUT_FILE = "episogram_data_mini.json"

	var width = 500,
		height = 2000;

	// set up svg
	var epis_svg = d3.select("#episogram").append("svg")
    	.attr("width", width)
    	.attr("height", height)
  		
	// load in the data
	d3.json(INPUT_FILE , function(data){
		
		// create a semester line
		var semester = addHorizLine( epis_svg , "semester" , weeksInSemester( data ) );

		// semester event listener
		semester.on("click" , function(week){
			fillTable(week);

			clearLines("week");
			clearLines("day");
			clearLines("asdf");
			
			var week_line = addVertiLine( epis_svg , "week" , daysInWeek( data ) , week );

			week_line.on("click" , function(day){
				
				clearLines("day")
				clearLines("asdf")
				var next_line = addHorizLine( epis_svg , "day" , daysInWeek( data ) , week , day );

				next_line.on("click" , function(d){
				
					clearLines("asdf")
					addVertiLine( epis_svg , "asdf" , daysInWeek( data ) , day , d );
				});
			});
			

		});
		

		/*
		// create a semester line given number of weeks
		var semester_line = createSemesterLine( epis_svg , num_weeks );

		// on circle clicks, semester line should open up a week line
		semester_line.on("click" , week => clickWeekNode( week , data , epis_svg ) );

		// click on day nodes
		*/

	});	
	
}

main();
