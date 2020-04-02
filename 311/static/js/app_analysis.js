
///////////////////////////////////////////////////////////////////////////////////////
///  The following code will populate the year dropdown based on the year chosen.
///  It is called for the zipcode function which is in turn called when
///  someone click on type of service dropdown on the analysis page.
///////////////////////////////////////////////////////////////////////////////////////

var zip_url = "/api/v1.0/getAllZipCodes"
var date_url = "/api/v1.0/getAllDates"
var serv_url = "/api/v1.0/getAllTypes"
var neib_url = "/api/v1.0/getAllNeib"

var selYear = 'ALL';
var selZip = 'ALL';
var selNeib = 'ALL';
var selType = 'ALL';

//////////////////////////////////////////////////////////////
// Zipcode selection dropdown - populates the zipcode dropdown
/////////////////////////////////////////////////////////////

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

//////////////////////////////////////////////////////////////////////
// Type of Service selection dropdown - populates the Type dropdown
/////////////////////////////////////////////////////////////////////

d3.json(serv_url).then(function(data) {
  var typeData = data;

  var sel = document.getElementById('selType');

  // clear out any data that was already there
  sel.innerHTML="";

  // sort the list of cities

  var firstOne = true;
  var opt = document.createElement('option');
  // create text node to add to option element (opt)
  opt.appendChild(  document.createTextNode('ALL') );
  // set value property of opt
  opt.value = 'ALL'; 
  // add opt to end of select box (sel)
  sel.appendChild(opt); 

  typeData.forEach(function(item) {
    var dataItem = item;
   
    // create new option element
    var opt = document.createElement('option');
    // create text node to add to option element (opt)
    opt.appendChild( document.createTextNode(dataItem) );
    // set value property of opt
    opt.value = dataItem; 
    // add opt to end of select box (sel)
    sel.appendChild(opt); 
  });
});


function showCensusdata() {
  var urlUse = "/api/v1.0/census/zipcode/" + selZip;
  console.log(urlUse);

  d3.json(urlUse).then(function(resp) {
    console.log("resp");
    console.log(resp);
    // var populationFormat = numeral(data.population).format('0,0');
    // var populationToPrint =`Population: ${populationFormat}`;
    // var unemploymentFormat = numeral(data.unemployment_rate/100).format('0.0%');
    // var unemployToPrint = `Unemployment Rate: ${unemploymentFormat}`;
    // var incomeFormat = numeral(data.median_income).format('$0,0');
    // var incomeToPrint = `Median Income: ${incomeFormat}`;
    // var homeFormat = numeral(data.median_value).format('$0,0');
    // var homeToPrint = `Median Home Value: ${homeFormat}`;


    var medianAge = resp[0].MedianAge
    var ageToPrint = `Median Age: ${medianAge}`;
    var householdIncome = numeral(resp[0].HouseholdIncome).format('$0,0');
    var incomeToPrint = `Household Income: ${householdIncome}`;
    var popu =  numeral(resp[0].Population).format('0,0');
    var popuPrint = `Population: ${popu}`;
    var househ = numeral(resp[0].TotalHouseholds).format('0,0');
    var househPrint = `Total Households : ${househ}`;
    var pove = numeral(resp[0].PovertyRate/100).format('0.0%');
    var povePrint = `Poverty Rate: ${pove}`;
    var perownocc =  numeral(resp[0].PerOwnerOccupied/100).format('0.0%');
    var perownoccPrint = `%age Owner Occupied: ${perownocc}`;

    // Clear out any data that was already in the key info area
    var selInfo = document.getElementById('censusData');

    selInfo.innerHTML="<br><br>";

    d3.select("#censusData")
        .append("h4")
        .text(incomeToPrint)
        .append("p")
        .text(ageToPrint)
        .append("p")
        .text(popuPrint)
        .append("p")
        .text(househPrint)
        .append("p")
        .text(perownoccPrint)
        .append("p")
        .text(povePrint)
        .append("p");
  });
}

showTop10Chart();
showByMonthChart();


function zipSelected(zipChosen) {
  selZip = zipChosen
  showTop10Chart();
  showByMonthChart();
  showCensusdata();
}

function yearSelected(yearChosen) {
  selYear = yearChosen
  showTop10Chart();
  showByMonthChart();
}

function typeSelected(typeChosen) {
  selType = typeChosen
  if (typeChosen === 'ALL') {
    showTop10Chart();
  }
  showByMonthChart();
}

