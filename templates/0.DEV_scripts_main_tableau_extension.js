'use strict';

// Function to use in Tableau Configuration or in General

//
  async function workSheetObjectOfSummaryTable() {

    const worksheets = tableau.extensions.dashboardContent.dashboard.worksheets;

    // Find summary_table worksheet
    const worksheet = worksheets.find(function (sheet) {
      return sheet.name === "summary_table";
    });

    return worksheet;
  }
//
  async function clog() {
      worksheet= await workSheetObjectOfSummaryTable() 
      console.log(worksheet.name); 
        
  }
  

// Tableau Configuration Function
 
function tableauConfig() {

    document.addEventListener('DOMContentLoaded', ()=>{
          
        tableau.extensions.initializeAsync().then(function () {

         clog();  
        }
        , function (err) {
            // Something went wrong in initialization.
            console.log('Error while Initializing: ' + err.toString());
        });
          

        });
};

tableauConfig();
