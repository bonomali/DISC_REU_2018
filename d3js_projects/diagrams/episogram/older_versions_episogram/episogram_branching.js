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

	return num_weeks;
}

//~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
// create the semester line given a certain amount of weeks
function createSemesterLine( svg , weeks ){
	
	// add main semester line
	svg.append("line")
		.attr("class" , "semester_line")
		.attr("x1" , 0)
		.attr("x2" , 500)
		.attr("y1" , 50)
		.attr("y2" , 50)
		.attr("stroke" , "blue")
		.attr("stroke-width" , "2")

	// create an array from 0 to number of weeks ( for data() )
	weeks_array = [];
	for(var i = 1; i <= weeks; i++)
		weeks_array.push(i);

	// add week nodes
	var week_nodes = svg.selectAll(".week_node")
		.data( weeks_array ).enter()
		.append("circle")
		.attr("class" , "week_node")
		.attr("cx" , week => week * 25 - 10)
		.attr("cy" , 50)
		.attr("r" , 10)
		.attr("fill" , "red");

	return week_nodes;

}

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

function clearLines(){
	d3.selectAll(".day_node")
		//.transition()
		.attr("r" , 0)
		.remove();

	d3.selectAll(".week_line")
		.transition()
		.attr("y2" , 50)
		.remove();
}

//~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
function main(){

	// variables and constants
	const INPUT_FILE = "json_files/episogram_data_mini.json"

	var width = 500,
		height = 2000;

	// set up svg
	var epis_svg = d3.select("#episogram").append("svg")
    	.attr("width", width)
    	.attr("height", height)
  		
	// load in the data
	d3.json(INPUT_FILE , function(data){
		
		// find number of weeks
		var num_weeks = weeksInSemester(data);

		// create a semester line given number of weeks
		var semester_line = createSemesterLine( epis_svg , num_weeks );

		// on circle clicks, semester line should open up a week line
		semester_line.on("click" , week => clickWeekNode( week , data , epis_svg ) );

		// click on day nodes
		

/*
		// turn data into array of objects
		newData = [];
		Object.keys(data).forEach( function(key){
			newData.push( data[key] );
		});

		console.log(newData);

		function getY( newData , student ){
			console.log(newData.indexOf(student));
			return newData.indexOf(student) * 50 + 50;
		}

		function getX( assignment ){
			console.log(assignment);
			return assignment.week * 25;
		}

		// add main timeline of semester
		var semester_lines = epis_svg
			.selectAll(".semester_line").data( newData ).enter()
			.append("line")
				.attr("class" , "semester_line")
				.attr("x1" , 0)
				.attr("x2" , 500)
				.attr("y1" , student => getY( newData , student ) )
				.attr("y2" , student => getY( newData , student ) )
				.attr("stroke" , "blue")
				.attr("stroke-width" , "2");

		// add timeline of the week
		for( var i = 0; i < newData.length; i++){
			
			var student = newData[i];

			epis_svg
				.selectAll(".week_line").data( student ).enter()
				.append("line")
					.attr("class" , "week_line")
					.attr("id" , newData.indexOf(student) )
					.attr("x1" , assignment => getX(assignment) )
					.attr("x2" , assignment => getX(assignment) )
					.attr("y1" , student => getY( newData , student ) )
					.attr("y2" , i * 50 + 50 )
					.attr("stroke" , "red")
					.attr("stroke-width" , "2");
		}
*/
	});	
	
}

main();
