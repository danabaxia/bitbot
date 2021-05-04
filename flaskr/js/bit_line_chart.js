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
            height:320,
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
            chartArea: { width: '85%', height:'75%'}

      };

      var chart = new google.visualization.LineChart(document.getElementById('chart_btc'));
      chart.draw(data, options);
    }