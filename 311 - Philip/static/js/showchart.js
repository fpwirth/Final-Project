function showByMonthChart(selectedZip, selectedYear, selectedType) {

    urlUse = urlM + '/zip/' + selZip;
    urlUse = urlUse + '/year/' + selYear;
    urlUse = urlUse + '/neib/' + selNeib;
    urlUse = urlUse + '/type/' + selType;
  
    d3.json(urlUse).then(function(typeData) {
  
     
      monthArray = [];
      countArray = [];
      tempArray = [];
      precArray = [];
      timeArray = [];
      overdueArray = [];
      
      typeData.forEach(function(data) {
      //   console.log("here is the data:", weatherData);
      monthArray.push(data.date_month);
      countArray.push(data.count_issues);
      precArray.push(data.prec);
      tempArray.push(data.avg_max);
      overdueArray.push(data.overdue);
      timeArray.push(data.time_taken);
      });
      console.log(timeArray)
      console.log(overdueArray)
          // Create our first trace
          var trace1 = {
            x: monthArray,
            y: tempArray,
            type: 'scatter',
            name: "Max Temp",
            yaxis: 'y3',
            marker: {
              color: 'rgb(255,0,0)'
            }
          };
      
          // Create our second trace 
          var trace2 = {
            x: monthArray,
            y: precArray,
            type: 'scatter',
            name: "Rainfall",
            yaxis: 'y2',
            marker: {
              color: 'rgb(0,0,255)'
            }
          };
          var trace3 = {
            x: monthArray,
            y: countArray,
            type: 'bar',
            name: "Service Issues",
            marker: {
              color: 'rgb(0,255,0)'
            }
          };
      
          var data = [trace1, trace2, trace3];
      
          var layout = {
              title: "311 Data",
            xaxis: { 
                title: {text:'Months',font:{ color: 'rgb(102,255,178)', size: 15 } },
                tickfont: {
                  color: 'white',
                },
                domain:[0.25, 0.9]
                },
            yaxis: { 
                    title: {text:'Number of Issues',font:{ color: 'rgb(102,255,178)', size: 15 } },
                    autorange: true, 
                    tickfont: {
                      color: 'white',
                    },
                    gridcolor:"white"
    
                   },
            yaxis2: {
                title: {text:'Precipitation',font:{ color: 'rgb(102,255,178)', size: 15 } },
                // titlefont: {color: '#ff7f0e'},
                // tickfont: {color: '#ff7f0e'},
                anchor: 'free',
                overlaying: 'y',
                side:"left",
                position:0.15,
                range: [0,20],
                autorange: false,
                tickfont: {
                  color: 'white',
                },
              },
            yaxis3: {
              title: {text:'Temperature',font:{ color: 'rgb(102,255,178)', size: 15 } },
              // titlefont: {color: '#ff7f0e'},
              // tickfont: {color: '#ff7f0e'},
              anchor: 'free',
              overlaying: 'y',
              side: 'right',
              range: [0,100],
              autorange: false,
              tickfont: {
                color: 'white',
              },
              position: .95
          },
            plot_bgcolor: "rgb(6, 38, 53)",
            paper_bgcolor:"rgb(6, 38, 53)",
           }; 
    
      Plotly.newPlot('lineChartMonth', data, layout);};