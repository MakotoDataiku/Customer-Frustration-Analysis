let default_colors = ['#FC427B','#16a085','#3498db','#9b59b6',
                      '#7ed6df','#3B3EAC','#0099C6','#DD4477',
                      '#66AA00','#B82E2E','#316395','#994499',
                      '#22AA99','#AAAA11','#6633CC','#E67300',
                      '#8B0707','#329262','#5574A6','#3B3EAC'];
setFilterOptions();

console.log($(document).ready(function() {
 $("#companies").select2();
}))

function onBarClicked(company, category) {
    let headers = new Headers();
    let init = {
        method : 'GET',
        headers : headers
    };
    let params = {
        'company':company,
        'category':category
    };
    console.log("stringify json", JSON.stringify(params))
    
    let url = getWebAppBackendUrl('/get_table')+'/'+JSON.stringify(params);
    let promise = fetch(url, init) 
                   .then(function(response) {
                       response.json()
                       .then(function(data){
                           let title_pos = 'Positive sentiment contributors for ' + company + " in " + category;
                           let title_neg = 'Negative sentiment contributors for ' + company + " in " + category;
                           document.getElementById('title_pos').innerHTML = title_pos;
                           document.getElementById('title_neg').innerHTML = title_neg;
                           //document.getElementById('table_stats_pos').innerHTML = data.table_pos;
                           //document.getElementById('table_stats_neg').innerHTML = data.table_neg;
                           console.log("data.table_pos", data["table_pos"])
                           addRows("table_stats_pos", data["table_pos"])
                       })
                   });
};




/*
document.getElementById("bar-chart-group").onclick = function(points, evt, barClicked) {
    console.log("Chart clicked", evt);
    console.log("points", points);
    console.log("barClicked", barClicked);
    if(points.length > 0){
        console.log("Bar chart clicked");
        console.log("Point", points[0].value);
    }
}
*/

/* returns the company value chosen from the dropdowns */
document.getElementById('button').onclick = function(){
    // let company = getSelectedOption('companies');
    let companies = $("#companies").val();
    console.log("company is", companies)
    let headers = new Headers()
    let init = {
        method : 'GET',
        headers : headers
    }
    let params = {
        'companies':companies
    }

    let url = getWebAppBackendUrl('/get_stats')+'/'+JSON.stringify(params)
    let promise = fetch(url, init) 
                   .then(function(response){
                       response.json()
                               .then(function(data){
                                // addBarChart(data.chart.data, data.chart.labels);
                           console.log("data.barChartGroup.company", data.barChartGroup.company)
                           console.log("data.barChartGroup.labels", data.barChartGroup.labels)
                                addGroupBarChart(data.barChartGroup.company, 
                                                 data.barChartGroup.labels);
                                })
                   });
}



function getSelectedOption(id){
/* function to get the selected value from the dropdowns */
    // let select = document.getElementById(id);
    // console.log("select is", select)
    // let value = select.options[select.selectedIndex].value;
    // console.log("selected comapnies are", value)
    // return value
    return $("#" + id).val();
}

/*
function getSelectedOption(id){
    
}
*/


function setFilterOptions(){
    /* function to get distinct values of companies and insert them in the dropdowns */
    let headers = new Headers()
    let init = {
        method : 'GET',
        headers : headers
    }

    let url = getWebAppBackendUrl('/get_filter_values')
    let promise = fetch(url, init)
                   .then(function(response){
                       response.json()
                               .then(function(data){
                                let companiesList = data.companies;
                                addOptions('companies', companiesList);                                
                                })
                   });
                       
}

function addRows(id, itemList){
    /* function to add rows to a table */
    let itemJson=JSON.parse(itemList)
    console.log("itemJson", typeof(itemJson))
    Object.keys(itemJson).forEach(function(key) {
        // this iterates over rows
        console.table('Key : ' + key + ', Value : ' + itemJson[key]);
        let topics = itemJson[key]["topics"]
        let averageScores = itemJson[key]["average scores"]
        let importanceScores = itemJson[key]["importance scores"]
        console.log("topics", topics)
        console.log("averageScores", averageScores)
        console.log("importanceScores", importanceScores)
        let tr = document.createElement('tr')
        let colTopic = document.createElement('th').innerHTML = topics
        let colAverageScores = document.createElement('th').innerHTML = averageScores
        let colImportanceScores = document.createElement('th').innerHTML = importanceScores
        let rowID = "row_" + key
        tr.setAttribute("id", rowID)
        document.getElementById(rowID).appendChild(colTopic)
        document.getElementById(rowID).appendChild(colAverageScores)
        document.getElementById(rowID).appendChild(colImportanceScores)
        document.getElementById(id).appendChild(tr)
})
    /*
    Object.keys(itemList).forEach(function(key){
        console.log("itemList", itemList)
        console.log("key", itemList[key])
        let topics = itemList[key]["topics"]
        let averageScores = itemList[key]["average scores"]
        let importanceScores = itemList[key]["importance scores"]
        console.log("topics", topics)
        let tr = document.createElement('tr')
        $tr.attr("id","")

    })
    itemList.forEach(function(value, index){
        let tr = document.createElement('tr');
        tr.text = value;
        document.getElementById(id).appendChild(tr)
    })
    */
}

function addOptions(id, itemList){
    /* function to add company choice to the dropdowns */
    itemList.forEach(function(value, index){
        let option = document.createElement('option');
        option.text = value;
        document.getElementById(id).appendChild(option)
    })
}

/*
function addBarChart(data, labels) {
    console.log("labels in addBarChart is", labels)
    document.getElementById('bar-card').innerHTML = '<canvas id="bar-chart" ></canvas>';
    new Chart(document.getElementById("bar-chart"), {
        type: "bar",
        data: {
          labels: labels,
          datasets: [{
            label: "Sentiment by category",
            data: data,
            backgroundColor: default_colors  
          }]
        },
        options: {
          title: {
            display: false,
            text: "Sentiment by category"
          }
        }
    });
}
*/

function addGroupBarChart(data, labels) {
    document.getElementById('bar-card').innerHTML = '<canvas id="bar-chart-group" chart-click="onClick"></canvas>';
    i = 1
    arr = []
    console.log("labels", labels)
    data.forEach(function(d){
        company = Object.keys(d);
        values = d[company]['data'];
        dataset_company = {
            label:company,
            backgroundColor: default_colors[i],
            data:values};
        console.log("dataset_company", dataset_company);
        arr.push(dataset_company);
        i+=1;
    })
    
    let data_grouped = {
        labels: labels,
        datasets: arr
              };
    
    // this.groupBarChart = 
    var chart = new Chart(document.getElementById("bar-chart-group"), {
        type: "bar",
        data: data_grouped,
        options: {
          title: {
            display: false,
            text: "Sentiment by category"
          },
            onClick: event => {
                const datasetIndex = chart.getElementAtEvent(event)[0]._datasetIndex;
                const model = chart.getElementsAtEvent(event)[datasetIndex]._model;
                onBarClicked(model.datasetLabel, model.label);
            }
        }
    });
}