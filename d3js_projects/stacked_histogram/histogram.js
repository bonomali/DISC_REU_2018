function makeHistogram(){

var svg4 = d3.select('#histogram').select("svg"),
    margin = {top: 0, right: 20, bottom: 20, left: 0},
    width = +svg4.attr("width") - margin.left - margin.right,
    height = +svg4.attr("height") - margin.top - margin.bottom,
    g = svg4.append("g").attr("transform", "translate(" + margin.left + "," + margin.top + ")");
var x = d3.scaleBand()
    .rangeRound([width/2, width])
    .paddingInner(0.05)
var x1 = d3.scaleBand()
	.rangeRound([0, width/2])
    .padding(0.05);

var y = d3.scaleLinear()
    .rangeRound([height, 0]);

var z = d3.scaleOrdinal()
    .range(["#98abc5", "#8a89a6", "#7b6888", "#6b486b", "#a05d56", "#d0743c", "#ff8c00"]);

var stack = d3.stack()
    .offset(d3.stackOffsetExpand);


// ** Update student display based on raw input

var nValue1 = 1;
var nValue2 = 1;

d3.select("#nValue1").on("input", function() {
  nValue1 = this.value
  update(+this.value, nValue2);
});

d3.select("#nValue2").on("input", function() {
  nValue2 = this.value
  update(nValue1, +this.value);
});

// Initial update value 
update(1, 1);


// adjust the text
function update(nValue1, nValue2) {
  var name_number1 = nValue1;
  var name_number2 = nValue2;
  compare_students(name_number1, name_number2);
}


/***************************************************************************
                              COMPARISON VIEW
***************************************************************************/
function compare_students(name_number1, name_number2) {
d3.select("#histogram").selectAll("g > *").remove();
console.log("num1="+name_number1.toString());
console.log("num2="+name_number2.toString());
d3.csv("csv_files/histogram.csv", function(d, i, columns) {
  for (i = 1, t = 0; i < columns.length; ++i) t += d[columns[i]] = +d[columns[i]];
  d.total = t;
  return d;
  }, function(error, Originaldata) {
  if (error) throw error;

  var name1 = "student" + name_number1 + "_"
  var name2 = "student" + name_number2 + "_"

  function filterCriteria1(d) {
    return d.student_assignment_grade.includes(name1);
  }
  function filterCriteria2(d) {
    return d.student_assignment_grade.includes(name2);
  } 
 
  var data1 = Originaldata.filter(filterCriteria1);
  var data2 = Originaldata.filter(filterCriteria2);
  var dict = {"Capstone":0,"ePortfolio Link":1,"Integration3":2,"Prompt1":3,"Prompt2":4,
  "Prompt3":5,"Prompt4":6,"Prompt5":7,"Prompt6":8,"Prompt7":9,"Prompt8":10,
  "Prompt9":11,"Prompt10":12,"Prompt11":13};
  var i;
  for (i = 0; i < data1.length; i++) {
	var tmp = data1[i].student_assignment_grade;
	var arr = tmp.split('_');
    data1[i].student_assignment_grade = "A"+dict[arr[1]];
	data1[i].grade = arr[2];
	data1[i].no = dict[arr[1]];
  }
  if (name_number1 != name_number2){
	for (i = 0; i < data2.length; i++) {
		var tmp = data2[i].student_assignment_grade;
		var arr = tmp.split('_');
		data2[i].student_assignment_grade = "A"+dict[arr[1]];
		data2[i].grade = arr[2];
		data2[i].no = dict[arr[1]];
	}
  }

  var keys = Originaldata.columns.slice(1);
  data1.sort(function(a,b){ return a.no - b.no; });
  data2.sort(function(a,b){ return b.no - a.no; });
  console.log(data1);
  console.log(data2);
  x.domain(data1.map(function(d) { return d.student_assignment_grade; }));
  x1.domain(data2.map(function(d) { return d.student_assignment_grade; }));
  var a = d3.max(data1, function(d) { return d.total; });
  var b = d3.max(data2, function(d) { return d.total; });
  var c = a>b?a:b;
  y.domain([0, c]).nice();
  z.domain(keys);
  d = d3.stack().keys(keys)(data1);
  d1 = d3.stack().keys(keys)(data2);
  
   g.append("g")
    .selectAll("g")
    .data(d)
    .enter()
	.append("g")
    .attr("fill", function(d) { return z(d.key); })
    .selectAll("rect")
    .data(function(d) { return d; })
    .enter()
	.append("rect")
      .attr("x", function(d) { return x(d.data.student_assignment_grade); })
      .attr("y", function(d) { return y(d[1]); })
      .attr("height", function(d) { return y(d[0]) - y(d[1]); })
      .attr("width", x.bandwidth());
	 
	g.append("g")
    .selectAll("g")
    .data(d1)
    .enter().append("g")
    .attr("fill", function(d) { return z(d.key); })
    .selectAll("rect")
    .data(function(d) { return d; })
    .enter()
	.append("rect")
      .attr("x", function(d) { return x1(d.data.student_assignment_grade); })
      .attr("y", function(d) { return y(d[1]); })
      .attr("height", function(d) { return y(d[0]) - y(d[1]); })
      .attr("width", x1.bandwidth());
	  
	 g.append("g")
	  .selectAll("text")
	  .data(data1)
	  .enter()
	  .append("text")
	  .attr("x", function(d) { return x(d.student_assignment_grade);})
	  .attr("y",function(d){ 
		return y(d.total)-3;
	  })
	  .attr("dy","0.32em")
	  .text(function(d){
			return d.grade;
	  });
	  
	 g.append("g")
	  .selectAll("text")
	  .data(data2)
	  .enter()
	  .append("text")
	  .attr("x", function(d) { return x1(d.student_assignment_grade);})
	  .attr("y",function(d){ 
		return y(d.total)-3;
	  })
	  .attr("dy","0.32em")
	  .text(function(d){
			return d.grade;
	  });
	  
  g.append("g")
      .attr("class", "axis")
      .attr("transform", "translate(0"  +"," + height + ")")
      .call(d3.axisBottom(x));

 g.append("g")
      .attr("class", "axis")
      .attr("transform", "translate(0"  +"," + height + ")")
      .call(d3.axisBottom(x1));

  g.append("g")
      .attr("class", "axis")
	  .attr("transform", "translate("+ width/2 +",0" + ")")
      .call(d3.axisLeft(y).ticks(null, "s"))
	  .append("text")
      .attr("x", -18)
	  .attr("y", 0)
      .attr("dy", "0.32em")
      .attr("font-weight", "bold")
      .attr("text-anchor", "end")
      .text("Number of instances");

  var legend = g.append("g")
      .attr("font-family", "sans-serif")
      .attr("font-size", 10)
      .attr("text-anchor", "end")
    .selectAll("g")
    .data(keys.slice().reverse())
    .enter().append("g")
      .attr("transform", function(d, i) { return "translate(0," + i * 20 + ")"; });

  legend.append("rect")
      .attr("x", width - 19)
      .attr("width", 19)
      .attr("height", 19)
      .attr("fill", z);

  legend.append("text")
      .attr("x", width - 19)
	  .attr("y", 9.5)
      .attr("dy", "0.32em")
      .text(function(d) { return d; });
});
};



/***************************************************************************
                               AGGREGATE VIEW
***************************************************************************/
function aggregate() {
d3.select("#histogram").selectAll("g > *").remove();
d3.csv("csv_files/grade_structures.csv", function(d, i, columns) {
  for (i = 1, t = 0; i < columns.length; ++i) t += d[columns[i]] = +d[columns[i]];
  d.total = t;
  return d;
}, function(error, data) {
  if (error) throw error;
  
  console.log(data);
  var keys = data.columns.slice(1);

  data.sort(function(a, b) { return b.total - a.total; });
  x.domain(data.map(function(d) { return d.grade; }));
  y.domain([0, d3.max(data, function(d) { return d.total; })]).nice();
  z.domain(keys);

  g.append("g")
    .selectAll("g")
    .data(d3.stack().keys(keys)(data))
    .enter().append("g")
      .attr("fill", function(d) { return z(d.key); })
    .selectAll("rect")
    .data(function(d) { return d; })
    .enter().append("rect")
      .attr("x", function(d) { return x(d.data.grade); })
      .attr("y", function(d) { return y(d[1]); })
      .attr("height", function(d) { return y(d[0]) - y(d[1]); })
      .attr("width", x.bandwidth());

  g.append("g")
      .attr("class", "axis")
      .attr("transform", "translate(0," + height + ")")
      .call(d3.axisBottom(x));

  g.append("g")
      .attr("class", "axis")
      .call(d3.axisLeft(y).ticks(null, "s"))
    .append("text")
      .attr("x", 2)
      //.attr("y", y(y.ticks().pop()) + 0.5)
      .attr("dy", "0.32em")
      .attr("fill", "#000")
      .attr("font-weight", "bold")
      .attr("text-anchor", "start")
      .text("Number of instances");

  var legend = g.append("g")
      .attr("font-family", "sans-serif")
      .attr("font-size", 10)
      .attr("text-anchor", "end")
    .selectAll("g")
    .data(keys.slice().reverse())
    .enter().append("g")
      .attr("transform", function(d, i) { return "translate(0," + i * 20 + ")"; });

  legend.append("rect")
      .attr("x", width - 19)
      .attr("width", 19)
      .attr("height", 19)
      .attr("fill", z);

  legend.append("text")
      .attr("x", width - 24)
      .attr("y", 9.5)
      .attr("dy", "0.32em")
      .text(function(d) { return d; });
});
};


d3.select("#histogram_info").selectAll("input[name=filter]").on("change", function(d){

  // value of selected radio
  var value = this.value;

	switch (value) {
		case "aggregate":
			aggregate();
			break;
		case "two":
			compare_students(name_number);
			break;
	default:
			aggregate();
	}

});
}
makeHistogram();