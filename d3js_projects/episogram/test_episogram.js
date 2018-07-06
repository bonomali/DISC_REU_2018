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
 * Graph Layout
 *
 *	
 *			   |
 *			   |
 *		assignments done this week
 *		click assign to see data
 *			   #
 *			   |
 *			   |
 *	weeksInSem-*------*--------*--------*--------*----------*----->
 *
 *************************************************************************/

// constants
const INPUT_FILE = "episogram_data_mini.json";
const INPUT_WEEKS = "assignments_by_week.json"
const SPACING = 25;
const BASE_Y = 400;
const BASE_NODE_RAD = 7;
const WEEK_HEIGHT = 200; /* WEEK_HEIGHT must be less than BASE_Y */

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

//~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
// adds vertical week lines to array given a week object
// that holds an array of assignment data
function addWeekLine( svg , weekAssigns ){

	const NAME = 4;
	
	Object.keys(weekAssigns).forEach( function(assign){

		// add a vertical line for week
		svg.append("line")
			.attr("class" , "week_line")
			.attr("x1" , parseInt(assign , 10) * SPACING + SPACING)
			.attr("x2" , parseInt(assign , 10) * SPACING + SPACING)
			.attr("y1" , BASE_Y - BASE_NODE_RAD)
			.attr("y2" , BASE_Y - WEEK_HEIGHT)
			.attr("stroke" , "blue")
			.attr("stroke-width" , "2");
	});
	
}

//~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
//
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

	// data loaded in should be an object of students
	// students are arrays of assignment objects
	d3.json(INPUT_FILE , function(assignsByStudent){

		// create a baseline (rewrite w/ assignsByWeek)
		var baseLine = createBaseLine( epis_svg , assignsByStudent );
	
		// get the data formatted by week (python?)
		// ie assignmentsByWeek = [ { week : [ assign ] } , ... ]
		d3.json(INPUT_WEEKS , function(assignsByWeek){
			
			// for each week node, create a line of assignment nodes
			assignsByWeek.forEach( function(week){
				addWeekLine( epis_svg , week );
			});

			// add hover data to base week node
			baseLine.on("click" , function(week_num){
			
				/* display summary of week data
				 * including:
				 *	unique assignments names
				 *	number of people that attempted them
				 */

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
	

}

main();







/*************************************************************************
 * Necessary fxns:
 *		
 *		addBaseLine( .... )
 *			- creates a base line for the diagram
 *
 * 		addHorizLine( className , arrayOfinfo )
 * 			- creates a horizontal line of a certain class using array
 *
 * 		addVertiLine( className , arrayOfInfo )
 * 			- creates a vertical line of a certain class using array
 *
 * 		createEpisogram( arrayOfClassNames , arrayOfData , xStart = 0 , yStart = 0 )
 * 			- creates an episogram with arrayOfClassNames.length lines and 
 * 			  uses info from array of data
 *
 *************************************************************************/
/*
//~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
function addHorizLine( svg , className , data , x = 0 , y = 0 ){

	// define class names
	var lineClass = className + "_line";
	var nodeClass = className + "_node";

	// add horiz line
	svg.append("line")
		.attr("class" , lineClass)
		.attr("x1" , x )//* 25)
		.attr("x2" , x + 500)//* 25 + 500)
		.attr("y1" , y )//* 25 + 10)
		.attr("y2" , y )//)* 25 + 10)
		.attr("stroke" , "blue")
		.attr("stroke-width" , "2");

	// add nodes
	var epis_nodes = svg.selectAll( nodeClass )
		.data( data ).enter()
		.append("circle")
		.attr("class" , nodeClass)
		.attr("cx" , d => d * 25 + x)//(x * 25) )
		.attr("cy" , y)//+ 10)
		.attr("r" , 10)
		.attr("fill" , "red");

	// add click functionality
	

	return epis_nodes
}d3.json(INPUT_FILE , function(data){


//~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
function addVertiLine( svg , className , data , x = 0 , y = 0 ){

	// define class names
	var lineClass = className + "_line";
	var nodeClass = className + "_node";

	// add verti line
	svg.append("line")
		.attr("class" , lineClass)
		.attr("x1" , x )//* 25 )
		.attr("x2" , x )//* 25 )
		.attr("y1" , y)
		.attr("y2" , y + 200)
		.attr("stroke" , "blue")
		.attr("stroke-width" , "2")

	// add nodes
	var epis_nodes = svg.selectAll( nodeClass )
		.data( data ).enter()
		.append("circle")
		.attr("class" , nodeClass)
		.attr("cx" , x)
		.attr("cy" , d => d * 25 + y )
		.attr("r" , 10)
		.attr("fill" , "red");

	return epis_nodes
}

/*~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
function createEpisogram( svg , classNames , data , x = 10, y = 0 ){

	var horizLine = false;
	var a;

	// create lines
	classNames.forEach( function(className){
		
		// create a baseline
		if( className === classNames[0] ){
			a = addHorizLine( svg , className , data , x , y )
		}

		// add other lines
		else{
			
			if(horizLine){
				a = addHorizLine( svg , className , data , x , y );
				x += 50;
				horizLine = false;
			}

			else{
				a = addVertiLine( svg , className , data , x , y );
				y += 50;
				horizLine = true;
			}

		}
		
		// add click function for each line
		a.on("click" , function( d ){

			// clear all lines after the class
			for(var i = 0; i < classNames.length; i++){
				if

			}
		
			// add a new line 

		});

		// update values

	});


}
*/
/*

function daysInWeek( data ){

	return [ 1 , 2 , 3 , 4 , 5 , 6 , 7 ];

}

function fillTable( data ){
	// fill in data table
	d3.select("#table_date").text("");
	d3.select("#table_week").text(data);

}
*/
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
/*
function clearLine( className ){
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
		.on("dblclick" , function(d){
			clearLine("week");
			clearLine("day");
			clearLine("asdf");
		});
  		
	// load in the data
	d3.json(INPUT_FILE , function(data){

		//var classes = [ "a" , "b" , "c" , "d" ];

		//createEpisogram( epis_svg , classes , Object.keys(data) )


		// create a semester line
		var semester = addHorizLine( epis_svg , "semester" , weeksInSemester( data ) );

		// semester event listener
		semester.on("click" , function(week){
			fillTable(week);

			clearLine("week");
			clearLine("day");
			clearLine("asdf");
			
			var week_line = addVertiLine( epis_svg , "week" , daysInWeek( data ) , week * 25 );

			week_line.on("click" , function(day){
				
				clearLine("day")
				clearLine("asdf")
				var next_line = addHorizLine( epis_svg , "day" , daysInWeek( data ) , week * 25 , day * 25 );

				next_line.on("click" , function(d){
				
					clearLine("asdf")
					addVertiLine( epis_svg , "asdf" , daysInWeek( data ) , d * 25 + week * 25, day * 25 );
				});
			});
			
		});
		

		/*
		// create a semester line given number of weeks
		var semester_line = createSemesterLine( epis_svg , num_weeks );

		// on circle clicks, semester line should open up a week line
		semester_line.on("click" , week => clickWeekNode( week , data , epis_svg ) );

		// click on day nodes
		

	});	
	
}

main();

*/
