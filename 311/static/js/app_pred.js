////////////////////////////////////////////////////////////////////////////////////////
///  The following code will populate the year dropdown based on the date chosen.
///////////////////////////////////////////////////////////////////////////////////////


var zip_url = "/api/v1.0/getAllZipCodes"

var selYear = 'ALL';
var selZip = 'ALL';


d3.json(zip_url).then(function(data) {
  var zipData = data;


  // Get the element id for the zipcode dropdown
  var sel = document.getElementById('selZip');

  // clear out any data that was already there
  sel.innerHTML="";

  // sort the list of zipcodes

  var firstOne = true;

    var opt = document.createElement('option');
    // create text node to add to option element (opt)
    opt.appendChild(  document.createTextNode('ALL') );
    // set value property of opt
    opt.value = 'ALL'; 
    // add opt to end of select box (sel)
    sel.appendChild(opt); 

  zipData.forEach(function(item) {
    var zipC = item;
    // create new option element
    var opt = document.createElement('option');
    // create text node to add to option element (opt)
    opt.appendChild( document.createTextNode(zipC) );
    // set value property of opt
    opt.value = zipC; 
    // add opt to end of select box (sel)
    sel.appendChild(opt); 
  });
  
});





var urlMM = "/api/v1.0/processModel"

function runModel(szip, stemp, srain, stype) {

  urlUse = urlMM + '/zip/' + szip;
  urlUse = urlUse + '/temp/' + stemp;
  urlUse = urlUse + '/rain/' + srain;
  urlUse = urlUse + '/type/' + stype;
  console.log(urlUse);

  d3.json(urlUse).then(function(resp) {
    console.log("resp");
    console.log(resp);
    var medianAge = resp[0].MedianAge
    var ageToPrint = `Median Age: ${medianAge}`;
    var householdIncome = resp[0].HouseholdIncome;
    var incomeToPrint = `Household Income: ${householdIncome}`;

    var popu = resp[0].Population;
    var popuPrint = `Population: ${popu}`;
    // data_dict["PerCapitaIncome"] = census['Per Capita Income']
    // data_dict["PovertyRate"] = census['Poverty Rate']
    // data_dict["TotalHouseholds"] = census['Total Households']
    // data_dict["TotalOwnerOccupied"] = census['Total Owner Occupied']
    // data_dict["PerOwnerOccupied"] = census['% Owner Occupied']
    // data_dict['MedianAge'] = census['Median Age']


    var househ = resp[0].TotalHouseholds;
    var househPrint = `TotalHouseholds: ${househ}`;

    var pove = resp[0].PovertyRate;
    var povePrint = `Poverty Rate: ${pove}`;

    var perownocc = resp[0].PerOwnerOccupied;
    var perownoccPrint = `PerOwnerOccupied: ${perownocc}`;

    var prediction = resp[0].Prediction;
    var predictionToPrint  = '';
    if (prediction == 0){
      predictionToPrint = `Prediction: ${prediction} - Meet timeline`;
    } else {
      predictionToPrint = `Prediction: ${prediction} - DOES NOT timeline`;
    }
    // var homeFormat = numeral(data.median_value).format('$0,0');
    // var homeToPrint = `Median Home Value: ${homeFormat}`;
    
    // Clear out any data that was already in the key info area
    var selInfo = document.getElementById('keyInfo');

    showResult.innerHTML="";

    d3.select("#showResult")
        .append("h4")
        .text(predictionToPrint)
        // .append("p")
        // .text(incomeToPrint)
        // .append("p")
        // .text(ageToPrint)
        // .append("p")
        // .text(popuPrint)
        // .append("p")
        // .text(househPrint)
        // .append("p")
        // .text(perownoccPrint)
        // .append("p")
        // .text(povePrint)
        .append("p");

  });
}




