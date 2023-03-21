// Get the select elements
var graphTypeSelect = document.getElementById("graphType");
var columnSelect = document.getElementById("columnSelector");
var chartCanvas = document.getElementById("chartCanvas");

// Initialize the chart
var chart = null;

// Function to update the graph based on user selections
function updateGraph() {
  // Retrieve the selected values
  var selectedGraphType = graphTypeSelect.value;
  var selectedColumn = columnSelect.value;

  // Fetch data for the selected column
  fetchData(selectedColumn, function(data) {
    // Update or create the chart based on the selected graph type
    if (chart) {
      chart.destroy();
    }

    chart = new Chart(chartCanvas, {
      type: selectedGraphType,
      data: {
        labels: data.labels,
        datasets: [{
          label: selectedColumn,
          data: data.values,
        }]
      }
    });
  });
}

// Function to fetch data based on the selected column
function fetchData(selectedColumn, callback) {
  // Make an AJAX request to fetch the CSV data
  var xhr = new XMLHttpRequest();
  xhr.onreadystatechange = function() {
    if (xhr.readyState === XMLHttpRequest.DONE) {
      if (xhr.status === 200) {
        // Parse the CSV data
        var csvData = xhr.responseText;
        var parsedData = parseCSV(csvData);

        // Find the column index based on the column name
        var columnIndex = parsedData[0].indexOf(selectedColumn);

        // Extract the column data
        var labels = [];
        var values = [];
        for (var i = 1; i < parsedData.length; i++) {
          labels.push(parsedData[i][0]);
          values.push(parsedData[i][columnIndex]);
        }

        // Create the data object
        var data = {
          labels: labels,
          values: values
        };

        // Invoke the callback with the data
        callback(data);
      } else {
        console.error('Failed to fetch CSV data: ' + xhr.status);
      }
    }
  };

  xhr.open('GET', '/Users/yunka/Desktop/New folder (3)/fyp11/data_analysis/dataset/data.csv');
  xhr.send();
}

// Function to parse CSV data
function parseCSV(csvData) {
  var rows = csvData.split('\n');
  var data = [];
  for (var i = 0; i < rows.length; i++) {
    data.push(rows[i].split(','));
  }
  return data;
}