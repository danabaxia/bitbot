google.charts.load('current', {packages: ['corechart', 'line'],callback: 'drawCharts'});

function json2array(json_data){
  var obj = JSON.parse(json_data);
  var result = [];
  for(var i in obj){
    var d = new Date(i);
    var minute = d.getUTCMinutes();
    var hour = d.getUTCHours();
    var day = d.getUTCDate();
    var month = d.getUTCMonth();

    _date = month + "/" + day;
    //console.log(_date);
    result.push([_date, obj[i]])
  }
  return result;
}

function drawCharts() {
  
      console.log('btc chart');
      //day
      var data_d = new google.visualization.DataTable();
      data_d.addColumn('string', 'date');
      data_d.addColumn('number', 'Price');
      data_d.addRows(json2array(value_d));
     
      var data_m = new google.visualization.DataTable();
      data_m.addColumn('string', 'date');
      data_m.addColumn('number', 'Price');
      data_m.addRows(json2array(value_m));

      var data_y = new google.visualization.DataTable();
      data_y.addColumn('string', 'date');
      data_y.addColumn('number', 'Price');
      data_y.addRows(json2array(value_y));

      var data_all = new google.visualization.DataTable();
      data_all.addColumn('string', 'date');
      data_all.addColumn('number', 'Price');
      data_all.addRows(json2array(value_all));




      var options = {
            legend: {position: 'none'},
            height:320,
            hAxis: {
              curveType: 'function',
              textPosition: 'none',
              gridlines: {
                  color: 'transparent',
                  minSpacing: 100,
                  count:1
              },
              showTextEvery:100,
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
            chartArea: { width: '85%', height:'95%'}

      };

      var chart = new google.visualization.LineChart(document.getElementById('chart_btc'));
      chart.draw(data_d, options);

      document.getElementById('btc_d').addEventListener('click', function (){
        console.log('day data');
        var elem = document.getElementById('btc_change');
        elem.textContent = change_d;
        var a = parseFloat(elem.textContent)
        console.log(typeof a);
        if (a<0){
          elem.classList.remove('green');
          elem.textContent = elem.textContent + '%';
        }else {
          elem.textContent = '+' + elem.textContent + '%';
          elem.classList.add('green');
        }

        chart.draw(data_d, options);

      }, false);

      document.getElementById('btc_m').addEventListener('click', function (){
        console.log('month data');
        var elem = document.getElementById('btc_change');
        elem.textContent = change_m;
        var a = parseFloat(elem.textContent)
        console.log(typeof a);
        if (a<0){
          elem.classList.remove('green');
          elem.textContent = elem.textContent + '%';
        }else {
          elem.textContent = '+' + elem.textContent + '%';
          elem.classList.add('green');
        }
        chart.draw(data_m, options);
      }, false);

      document.getElementById('btc_y').addEventListener('click', function (){
        console.log('year data');
        var elem = document.getElementById('btc_change');
        elem.textContent = change_y;
        var a = parseFloat(elem.textContent)
        console.log(typeof a);
        if (a<0){
          elem.classList.remove('green');
          elem.textContent = elem.textContent + '%';
        }else {
          elem.textContent = '+' + elem.textContent + '%';
          elem.classList.add('green');
        }
        chart.draw(data_y, options);
      }, false);

      document.getElementById('btc_all').addEventListener('click', function (){
        console.log('all data');
        var elem = document.getElementById('btc_change');
        elem.textContent = change_all;
        var a = parseFloat(elem.textContent)
        console.log(typeof a);
        if (a<0){
          elem.classList.remove('green');
          elem.textContent = elem.textContent + '%';
        }else {
          elem.textContent = '+' + elem.textContent + '%';
          elem.classList.add('green');
        }
        chart.draw(data_all, options);
      }, false);


    };
