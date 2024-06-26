var bigDailyHTML;
var bigWeeklyHTML;
var tohDailyHTML;
var tohWeeklyHTML;

fetch('resultsOutput.txt')
    .then(response => response.text())
    .then(text => {
        var arr = text.split(",")
        setNums(arr)
        setVars(arr)
    })

function setVars(arr){
    bigDailyHTML = arr[2];
    bigWeeklyHTML = arr[3];
    tohDailyHTML = arr[4];
    tohWeeklyHTML = arr[5];
}

function setNums(arr){
    document.getElementById("firstRow").innerHTML = arr[0];
    document.getElementById("secondRow").innerHTML = arr[1];
    document.getElementById("thirdRow").innerHTML = arr[6] + ',' + arr[7];
}

function loadCharts(chartType){
    switch(chartType){
        case "bigDaily":
            loadTable(bigDailyHTML);
            break;
        case "bigWeekly":
            loadTable(bigWeeklyHTML);
            break;
        case "tohDaily":
            loadTable(tohDailyHTML);
            break;
        case "tohWeekly":
            loadTable(tohWeeklyHTML);
            break;
    }
}

function loadTable(html){
    document.getElementById("chartsTable").innerHTML = html;
}

function highlightBtn(selectedButton) {
    // Remove the 'highlighted' class from all buttons
    document.querySelectorAll('.btn').forEach(function(button) {
      button.classList.remove('highlighted');
    });
  
    // Add the 'highlighted' class to the clicked button
    selectedButton.classList.add('highlighted');
  }