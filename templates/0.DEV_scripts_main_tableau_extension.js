'use strict';

// Function to use in Tableau Configuration or in General
function clog(a) {
  // Function returns the product of a and b
    console.log(a); 
  }
  
// Tableau Configuration Function
 
async function tableauConfig() {

    document.addEventListener('DOMContentLoaded', ()=>{
          
        tableau.extensions.initializeAsync().then(function () {

          //Here you define your Tableau related code
          const worksheets = tableau.extensions.dashboardContent.dashboard.worksheets;

          // Find summary_table worksheet
          var worksheet = worksheets.find(function (sheet) {
            return sheet.name === "summary_table";
          });

          clog(worksheet.name);
          

          }
           , function (err) {
            // Something went wrong in initialization.
            console.log('Error while Initializing: ' + err.toString());
          });
          

        });
};

// Function in which you are going to define what to do after Tableau's Configuration

async function afterTableausConfiguration(){
  await tableauConfig();
  // now wait for tableauConfig to finish...
  clog("After Tableau's Configuration Test");

};

//Execute Functions

afterTableausConfiguration();