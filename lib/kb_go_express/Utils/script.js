var data1 = [];
var data2 = [];
var data3 = ['all'];




d3.json("out.json", function(d) {


data1 = d.conditions;
for (i=0; i<data1.length; i++){
	data2[i] = data1[i];
}


var temp = data2.shift()
data2.push(temp)
data3 = d.categories;

console.log('data1')

console.log(data1)


function get_table_data (condition1, condition2, category, d){

	if (condition1 == condition2){

		return ["<strong>Please select different conditions</strong>", ""];
	}




	if (typeof(category) != 'string'){
		condition1 = d.conditions[0];
		condition2 = d.conditions[1];
		category = d.categories[0];
	}

	image_data = "";
	
	table_data = "<table border =1>";
	table_data += "<tr>";
	table_data += "<th>go_id</th>";
	table_data += "<th>go_function</th>";
	table_data += "<th>e-value</th>";
	
	table_data += "<th>First condition</th>";
	table_data += "<th>Second condition</th>";
	table_data += "<th>Category</th>";

	table_data += "<th>Image</th>";

	table_data += "</tr>";
	rows = d.data;
	for (i = 0; i < rows.length; i++) {
		row = rows[i] ;



		if ((row.condition1 ==condition1 & row.condition2 == condition2) |
			(row.condition2 ==condition1 & row.condition1 == condition2)){

		if (row.namespace_1003 == category){

     	table_data  += "<tr>" ;
     	table_data += '<td>' + row.go_id + "</td>";
		table_data += '<td>' + row.name_1006 + "</td>";
		table_data += '<td>' + row.p_val + "</td>";

		table_data += '<td>' + condition1 + "</td>";
		table_data += '<td>' + condition2 + "</td>";
		table_data += '<td>' + row.namespace_1003 + "</td>";
		
		table_data += '<td>'  + '<a href = "#' + row.pathTOHMAP +  '">' + '<img src="' + row.pathTOHMAP  + '",height=20, width=100></a></td>';
     	table_data  += "</tr>" ;

		image_data +=  '<span id ="' + row.pathTOHMAP +  '">' + '<img src="' + row.pathTOHMAP  + '",height=500, width=500></span>';


}
}
}
	table_data += "</table>";

return [table_data, image_data];

}

var select1 = d3.select('div')
  .append('select')
  	.attr('class','select')
  	.attr('id', 'condition1')
    .on('change',onchange);

var options1 = select1
  .selectAll('option')
	.data(data1).enter()
	.append('option')
		.text(function (d) { return d; });

var select2 = d3.select('div')
  .append('select')
  	.attr('class','select')
  	.attr('id', 'condition2')
    .on('change',onchange);

var options2 = select2
  .selectAll('option')
	.data(data2).enter()
	.append('option')
		.text(function (d) { return d; });

var select3 = d3.select('div')
  .append('select')
  	.attr('class','select')
  	.attr('id', 'category')
    .on('change',onchange);

var options3 = select3
  .selectAll('option')
	.data(data3).enter()
	.append('option')
		.text(function (d) { return d; });

	data = get_table_data (condition1, condition2, category, d);
	tablehtml = data[0];
	imagehtml = data[1]

	document.getElementById("tabx").innerHTML= tablehtml;
document.getElementById("imgx").innerHTML= imagehtml;




function onchange() {
	condition1 = d3.select('#condition1').property('value');
	condition2 = d3.select('#condition2').property('value');
	category = d3.select('#category').property('value');
	
	data = get_table_data (condition1, condition2, category, d);
	tablehtml = data[0];
	imagehtml = data[1]
	document.getElementById("tabx").innerHTML= tablehtml;
document.getElementById("imgx").innerHTML= imagehtml;

}

});
