// Load google charts
google.charts.load('current', {'packages':['corechart']});
google.charts.setOnLoadCallback(drawChart);
      
// Draw the chart and set the chart values
function drawChart() {
    var data = google.visualization.arrayToDataTable([
    ['Task', 'Portfolio'],
    ['Cash', parseFloat(cash)],
    ['Bitcoin', parseFloat(bit)],
    ['Hedge Fund',parseFloat(hedge)]
    ]);
        
    // Optional; add a title and set the width and height of the chart
    var options = { 'width':450, 'height':350,
                    'colors':['#3C5CE4','#20CE20','#EDCA0E'],
                    'chartArea':{left:140,width:'100%'}
                  };
        
    // Display the chart inside the <div> element with id="piechart"
    var chart = new google.visualization.PieChart(document.getElementById('piechart'));
    chart.draw(data, options);
}
