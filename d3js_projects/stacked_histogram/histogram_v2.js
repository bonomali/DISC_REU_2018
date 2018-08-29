function makeHistogram(){
	
var dict = {"Capstone":0,"ePortfolio Link":1,"Integration3":2,"Prompt1":3,"Prompt2":4,
  "Prompt3":5,"Prompt4":6,"Prompt5":7,"Prompt6":8,"Prompt7":9,"Prompt8":10,
  "Prompt9":11,"Prompt10":12,"Prompt11":13};
var Originaldata;
var svg4 = d3.select('#histogram').select("svg"),
    margin = {top: 10, right: 0, bottom: 20, left: 0},
    width = +svg4.attr("width") - margin.left - margin.right,
    height = +svg4.attr("height") - margin.top - margin.bottom,
    g = svg4.append("g").attr("transform", "translate(" + margin.left + "," + margin.top + ")");
var x = d3.scaleLinear()
    .rangeRound([width/2, width]);
var x1 = d3.scaleLinear()
	.rangeRound([width/2, 0]);

var y = d3.scaleBand()
    .rangeRound([0, height])
	.paddingInner(0.05);

var z = d3.scaleOrdinal()
    .range(["#98abc5", "#8a89a6", "#7b6888", "#6b486b", "#a05d56", "#d0743c", "#ff8c00"]);

var stack = d3.stack()
    .offset(d3.stackOffsetExpand);


// ** Update student display based on raw input

var nValue1 = 1;
var nValue2 = 1;

d3.select("#nValue1").on("input", function() {
  nValue1 = this.value;
  distance_file = "csv_files/distance.csv";
  d3.csv(distance_file,function(error, data){
	data.forEach(function(d){
		if(d.number == nValue1){
			update(nValue1,d.farest);
			d3.select("#nValue2").attr("value",d.farest);
		}
	});
  });
});

d3.select("#nValue2").on("input", function() {
  nValue2 = this.value
  update(nValue1, +this.value);
});

d3.csv("csv_files/histogram_communities.csv", function(d, i, columns) {
  for (i = 1, t = 0; i < columns.length; ++i) t += d[columns[i]] = +d[columns[i]];
  d.total = t;
  return d;
  }, 
  function(error, data) {
	Originaldata = data;
	// Initial update value 
	update(1, 1);
});


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
d3.select("#histogram").selectAll("g>*").remove();
console.log("num1="+name_number1.toString());
console.log("num2="+name_number2.toString());

  var name1 = "student" + name_number1 + "_"
  var name2 = "student" + name_number2 + "_"

  function filterCriteria1(d) {
    return d.student_assignment_grade.includes(name1);
  }
  function filterCriteria2(d) {
    return d.student_assignment_grade.includes(name2);
  } 
 
  var data1 = JSON.parse(JSON.stringify(Originaldata.filter(filterCriteria1)));
  var data2 = JSON.parse(JSON.stringify(Originaldata.filter(filterCriteria2)));

  var i;
  for (i = 0; i < data1.length; i++) {
	var tmp = data1[i].student_assignment_grade;
	var arr = tmp.split('_');
    data1[i].student_assignment_grade = "A"+dict[arr[1]];
	data1[i].grade = arr[2];
	data1[i].no = dict[arr[1]];
  }

	for (i = 0; i < data2.length; i++) {
		var tmp = data2[i].student_assignment_grade;
		var arr = tmp.split('_');
		data2[i].student_assignment_grade = "A"+dict[arr[1]];
		data2[i].grade = arr[2];
		data2[i].no = dict[arr[1]];
	}

  var assign_name = ["A0","A1","A2","A3","A4","A5","A6","A7","A8","A9","A10","A11","A12","A13"];
  var keys = Originaldata.columns.slice(1);
  data1.sort(function(a,b){ return a.no - b.no; });
  data2.sort(function(a,b){ return a.no - b.no; });
  console.log(data1);
  console.log(data2);
  a = d3.max(data1, function(d){return d.total; });
  b = d3.max(data2, function(d){return d.total; });
  c = a>b?a:b;
  x.domain([0, c+5]);
  x1.domain([0, c+5]);
  y.domain(assign_name);
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
      .attr("y", function(d) { return y(d.data.student_assignment_grade); })
      .attr("x", function(d) { return x(d[0]); })
      .attr("width", function(d) { return x(d[1]) - x(d[0]); })
      .attr("height", y.bandwidth());
	 
	g.append("g")
      .selectAll("g")
      .data(d1)
      .enter().append("g")
      .attr("fill", function(d) { return z(d.key); })
      .selectAll("rect")
      .data(function(d) { return d; })
      .enter()
	  .append("rect")
      .attr("y", function(d) { return y(d.data.student_assignment_grade); })
      .attr("x", function(d) { return x1(d[1]); })
      .attr("width", function(d) { return x1(d[0]) - x1(d[1]); })
      .attr("height", y.bandwidth());
	  
	 g.append("g")
	  .selectAll("text")
	  .data(data1)
	  .enter()
	  .append("text")
	  .attr("x", function(d) { return x(d.total);})
	  .attr("y",function(d){ 
		return y(d.student_assignment_grade)+8;
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
	  .attr("x", function(d) { return x1(d.total)-15;})
	  .attr("y",function(d){ 
		return y(d.student_assignment_grade)+8;
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
      .attr("x", 0)
	  .attr("y", -5)
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
};



/***************************************************************************
                               AGGREGATE VIEW
***************************************************************************/
function aggregate() {
d3.select("#histogram").selectAll("g>*").remove();
d3.csv("csv_files/grades_communities.csv", function(d, i, columns) {
  for (i = 1, t = 0; i < columns.length; ++i) t += d[columns[i]] = +d[columns[i]];
  d.total = t;
  return d;
}, function(error, data) {
  if (error) throw error;
  
  console.log(data);
  var keys = data.columns.slice(1);
  var x = d3.scaleBand()
    .rangeRound([0, width])
    .paddingInner(0.05);
  var y = d3.scaleLinear()
    .rangeRound([height, 0]);
	
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
      .attr("x", width-19)
      .attr("width", 19)
      .attr("height", 19)
      .attr("fill", z);

  legend.append("text")
      .attr("x", width-19 )
      .attr("y", 9.5)
      .attr("dy", "0.32em")
      .text(function(d) { return d; });
});
};


d3.select("#histogram_info").selectAll("input[name=filter]").on("change", function(d){

  // value of selected radio
  var value = this.value;
  console.log(value);
	switch (value) {
		case "aggregate":
			aggregate();
			break;
		case "two":
			compare_students(nValue1,nValue2);
			break;
	default:
			aggregate();
	}

});
}
makeHistogram();
