'use strict';

// Functions to use in Tableau Configuration or in General

//Tableau Configuration and After

//
  async function tableauConfig() {

    const worksheets = tableau.extensions.dashboardContent.dashboard.worksheets;

    // Find summary_table worksheet
    const worksheet = worksheets.find(function (sheet) {
      return sheet.name === "summary_table";
    });


    const dataTableReader = await worksheet.getSummaryDataReaderAsync();
    const dataTable = await dataTableReader.getAllPagesAsync();
    await dataTableReader.releaseAsync();
  
    let maxValue=0
    let maxURL=""

    for (let i = 2; i < dataTable.totalRowCount; i += 3) {
  
  
      if (maxValue < dataTable.data[i][4]['_value']) {
        maxValue = dataTable.data[i][4]['_value'];
        maxURL=dataTable.data[i][1]['_value']
      }
    }
    document.getElementById("imageid").src=maxURL;
  
    console.log(maxURL)
    console.log(maxValue)

    let unregisterHandlerFunction = worksheet.addEventListener(tableau.TableauEventType.FilterChanged, console.log("jaja"));

    return unregisterHandlerFunction



  }
//
  async function afterTableauConfig() {
      event1= await tableauConfig()
      //Here define what you wanna do after  Tableau Configuration
      console.log("After Test")
      console.log(event1)
        
  }

// Tableau Configuration Function
 
function tableauInitialize() {

    document.addEventListener('DOMContentLoaded', ()=>{
          
        tableau.extensions.initializeAsync().then(function () {

         afterTableauConfig(); 
          
        }
        , function (err) {
            // Something went wrong in initialization.
            console.log('Error while Initializing: ' + err.toString());
        });
          

        });
};

tableauInitialize();
