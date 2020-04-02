////////////////////////////////////////////////////////////////////////////////////////
///  The following code will populate the year dropdown based on the date chosen.
///  It is called for the stateSelected function which is in turn called when
///  someone click on a new state in the state dropdown on the application page.
///////////////////////////////////////////////////////////////////////////////////////


var url = "http://localhost:5000/api/v1.0/houston311/top10Types"

function showTop10Chart() {

  urlUse = url + '/zip/' + selZip;
  urlUse = urlUse + '/year/' + selYear;
  urlUse = urlUse + '/neib/' + selNeib;
  urlUse = urlUse + '/type/ALL';
  
  d3.json(urlUse).then(function(typeData) {

   
    typeArray = [];
    countArray = [];
    
    typeData.forEach(function(data) {
    //   console.log("here is the data:", weatherData);
    typeArray.push(data.serv_type);
    countArray.push(data.count_issues);
    });
        // Create our first trace
        var trace1 = {
          x: typeArray,
          y: countArray,
          type: 'bar',
          name: "Service Issues",
          marker: {
            color: 'rgb(255,0,0)'
          }
        };
    
        var data = [trace1];
    
        var layout = {
            title: {text:"Top 10 Service Requests",font:{ color: 'rgb(96,255,170)', size: 18 } }, 
          xaxis: { 
              title: {text:'Type of Issue',font:{ color: 'rgb(102,255,178)', size: 15 } },
              tickfont: {
                color: 'white',
              },
              domain:[0.2, 0.9]
              },
          yaxis: { 
                  title: {text:'Number of Issues',font:{ color: 'rgb(102,255,178)', size: 15 } },
                  autorange: true, 
                  tickfont: {
                    color: 'white',
                  },
                  gridcolor:"white"
  
                 },
          plot_bgcolor: "rgb(6, 38, 53)",
          paper_bgcolor:"rgb(6, 38, 53)",
         }; 
  
   
    Plotly.newPlot('lineChart', data, layout);
  });
  
}

