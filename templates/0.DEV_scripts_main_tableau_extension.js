'use strict';

// Wrap everything in an anonymous function to avoid polluting the global namespace
(
 
 function () {

    document.addEventListener('DOMContentLoaded', ()=>{
        tableau.extensions.initializeAsync().then(function () {
            // Since dataSource info is attached to the worksheet, we will perform
            // one async call per worksheet to get every dataSource used in this
            // dashboard.  This demonstrates the use of Promise.all to combine
            // promises together and wait for each of them to resolve.
            const dataSourceFetchPromises = [];
      
            // Maps dataSource id to dataSource so we can keep track of unique dataSources.
            const dashboardDataSources = {};
      
            // To get dataSource info, first get the dashboard.
            const dashboard = tableau.extensions.dashboardContent.dashboard;
      
            // Then loop through each worksheet and get its dataSources, save promise for later.
            dashboard.worksheets.forEach(function (worksheet) {
              dataSourceFetchPromises.push(worksheet.getDataSourcesAsync());
            });
      
            Promise.all(dataSourceFetchPromises).then(function (fetchResults) {
              fetchResults.forEach(function (dataSourcesForWorksheet) {
                dataSourcesForWorksheet.forEach(function (dataSource) {
                  if (!dashboardDataSources[dataSource.id]) { // We've already seen it, skip it.
                    dashboardDataSources[dataSource.id] = dataSource;
                  }
                });
              });
      
              console.log(dashboardDataSources.toString());
      
              // This just modifies the UI by removing the loading banner and showing the dataSources table.

            });
          }, function (err) {
            // Something went wrong in initialization.
            console.log('Error while Initializing: ' + err.toString());
          });
    
    
        });
}

)();
