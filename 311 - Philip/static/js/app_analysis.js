
///////////////////////////////////////////////////////////////////////////////////////
///  The following code will populate the year dropdown based on the year chosen.
///  It is called for the zipcode function which is in turn called when
///  someone click on type of service dropdown on the analysis page.
///////////////////////////////////////////////////////////////////////////////////////

var zip_url = "http://localhost:5000/api/v1.0/getAllZipCodes"
var date_url = "http://localhost:5000/api/v1.0/getAllDates"
var serv_url = "http://localhost:5000/api/v1.0/getAllTypes"
var neib_url = "http://localhost:5000/api/v1.0/getAllNeib"

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
  var urlUse = "http://localhost:5000/api/v1.0/census/zipcode/" + selZip;
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
    var househ = resp[0].TotalHouseholds;
    var househPrint = `TotalHouseholds: ${househ}`;
    var pove = resp[0].PovertyRate;
    var povePrint = `Poverty Rate: ${pove}`;
    var perownocc = resp[0].PerOwnerOccupied;
    var perownoccPrint = `PerOwnerOccupied: ${perownocc}`;

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

