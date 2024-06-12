'use strict';

// Wrap everything in an anonymous function to avoid polluting the global namespace
(
 
 function () {

    document.addEventListener('DOMContentLoaded', ()=>{
          
        tableau.extensions.initializeAsync().then(function () {



          console.log(worksheet);


          }
           , function (err) {
            // Something went wrong in initialization.
            console.log('Error while Initializing: ' + err.toString());
          });
          

        });

        const worksheets = tableau.extensions.dashboardContent.dashboard.worksheets;

        // Find summary_table worksheet
        var worksheet = worksheets.find(function (sheet) {
          return sheet.name === "summary_table";
        });

}

)();
