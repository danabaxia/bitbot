/*pass data to this js  */
document.currentScript.getAttribute('data');

google.charts.load('current', {packages: ['corechart', 'line']});
google.charts.setOnLoadCallback(drawLogScales);

function drawLogScales() {
      var data = new google.visualization.DataTable();
      data.addColumn('number', 'X');
      data.addColumn('number', 'Dogs');

      data.addRows([
        [0, 100],    [1, 100],   [2, 150],  [3, 150],   [4, 200],  [5, 200]

      ]);

      var options = {
            legend: {position: 'none'},
            width: 1000,
            height:380,
            hAxis: {
              curveType: 'function',
              gridlines: {
                  color: 'transparent'
              },
              logScale: true
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

      var chart = new google.visualization.LineChart(document.getElementById('chart_div'));
      chart.draw(data, options);
    }