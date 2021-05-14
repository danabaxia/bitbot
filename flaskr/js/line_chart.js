google.charts.load('current', {packages: ['corechart', 'line'], callback:'drawLogScales'});
google.charts.setOnLoadCallback(drawLogScales);

var obj = JSON.parse(balance_dict)
console.log(obj)
var result = [];
for(var i in obj)
    result.push([i, obj [i]]);
console.log(result)

function drawLogScales() {
      var data = new google.visualization.DataTable();
      data.addColumn('string', 'Time');
      data.addColumn('number', 'Price');
      data.addRows(result);
      var options = {
            legend: {position: 'none'},
            width: 500,
            height:380,
            hAxis: {
              textPosition: 'none',
              curveType: 'function',
              gridlines: {
                  color: 'transparent',
                  minSpacing: 100,
              },
              logScale: false,
            },
            vAxis: {
                gridlines: {
                    color: 'black',
                    minSpacing: 100,
                    count:1
            },
            logScale: false
            },
            colors: ['blue'],
            chartArea: { width: '100%', height:'90%'}
      };

      var chart = new google.visualization.LineChart(document.getElementById('chart_balance'));
      chart.draw(data, options);
    }