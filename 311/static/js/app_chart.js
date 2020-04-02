////////////////////////////////////////////////////////////////////////////////////////
///  The following code will populate the year dropdown based on the year chosen.
///  It is called for the zipcode function which is in turn called when
///  someone click on type of service dropdown on the analysis page.
///////////////////////////////////////////////////////////////////////////////////////



var urlM = "/api/v1.0/houston311/ByMonth"

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
          title: {text:"Service types Average temperature and rainfall",font:{ color: 'rgb(96,255,170)', size: 18 } }, 
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
  
    Plotly.newPlot('lineChartMonth', data, layout);
  //  Plotly.plot(data, layout, function (err, msg) {
  //    console.log(msg);
  //    });

          // Create our first trace
          var trace1 = {
            x: monthArray,
            y: timeArray,
            type: 'scatter',
            yaxis: 'y3',
            name: "Time Taken",
            marker: {
              color: 'rgb(255,0,0)'
            }
          };
          var trace2 = {
            x: monthArray,
            y: overdueArray,
            type: 'scatter',
            yaxis: 'y2',
            name: "Overdue",
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
            title: {text:"Service types time to complete and overdue time",font:{ color: 'rgb(96,255,170)', size: 18 } }, 
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
                title: {text:'Overdue',font:{ color: 'rgb(102,255,178)', size: 15 } },
                anchor: 'free',
                overlaying: 'y',
                side: 'left',
                position: .15,
                autorange: true,
                tickfont: {
                  color: 'white',
                }
             },
             yaxis3: {
                  title: {text:'Issue Time',font:{ color: 'rgb(102,255,178)', size: 15 } },
                  anchor: 'free',
                  overlaying: 'y',
                  side: 'right',
                  position: .95,
                  autorange: false,
                  range: [0,20],
                  tickfont: {
                    color: 'white',
                  }
            },
            plot_bgcolor: "rgb(6, 38, 53)",
            paper_bgcolor:"rgb(6, 38, 53)",
           }; 
    
      Plotly.newPlot('lineChartMonth2', data, layout);
  });
  
}
