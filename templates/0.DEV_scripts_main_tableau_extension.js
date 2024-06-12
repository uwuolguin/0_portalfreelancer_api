'use strict';

// Function to use in Tableau Configuration or in General

//
  async function tableauConfig() {

    const worksheets = tableau.extensions.dashboardContent.dashboard.worksheets;

    // Find summary_table worksheet
    const worksheet = worksheets.find(function (sheet) {
      return sheet.name === "summary_table";
    });

    console.log(worksheet.name); 

  }
//
  async function afterTableauConfig() {
      await tableauConfig()
      //Here define what you wnna do after  Tableau Configuration
      console.log("After Test")


        
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
