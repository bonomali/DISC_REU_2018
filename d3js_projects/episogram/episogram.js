function main(){

	// variables and constants
	const INPUT_FILE = "episogram_data_mini.json"

	var width = 500,
		height = 200;

	// set up svg
	var epis_svg = d3.select("#episogram").append("svg")
    	.attr("width", width)
    	.attr("height", height)
  		
	// load in the data
	d3.json(INPUT_FILE , function(data){
		
		var num = 0;	
		Object.keys(data).forEach(function(student) {
    		console.log(student, data[student]);

			var y = num * 50 + 5

			/*var svg = epis_svg
				.append("svg")
				.attr("class" , "student_epis")
				.attr("width" , width)
				.attr("height" , height)
			*/
			var weeks_line = epis_svg.append("line")
				.attr("x1" , 0)
				.attr("x2" , 500)
				.attr("y1" , y)
				.attr("y2" , y)
				.attr("stroke" , "blue")
				.attr("stroke-width" , "2");

			data[student].forEach( function(assignment){
				epis_svg.append("circle")
					.attr("cx" , assignment.week * 25)
					.attr("cy" , y)
					.attr("r" , 5)
					.attr("fill" , "red");
			});

			num++;

		});
	});
	
	
}

main();
