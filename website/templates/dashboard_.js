function loadDataset() {
    var file = '/Users/yunka/Desktop/New folder (3)/fyp11/data_analysis/dataset/data.csv';
    var xhr = new XMLHttpRequest();
  
    xhr.onload = function() {
      if (xhr.status === 200) {
        var datasetContent = xhr.responseText;
        var dataset = parseCSV(datasetContent);
    
        displayFirstRow(dataset);
      } else {
        console.error('Failed to load the dataset. Status code: ' + xhr.status);
      }
    };
    
    xhr.open('GET', file, true);
    xhr.send();
  }
  
  function displayFirstRow(dataset) {
    var outputElement = document.getElementById('output');
  
    // Access the first row of the dataset
    var firstRow = dataset[0];
  
    // Convert the first row to a comma-separated string
    var firstRowString = firstRow.join(', ');
  
    // Print the first row
    outputElement.textContent = firstRowString;
  }