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
                           addRows("insert_table_pos", data["table_pos"]);
                           addRows("insert_table_neg", data["table_neg"]);
                           addRowHandlers(data["table_pos"]);
                       })
                   });
};

/*
function onTableClicked(company, category, topic) {
    let headers = new Headers();
    let init = {
        method : 'GET',
        headers : headers
    };
    let params = {
        'company':company,
        'category'category,
        'review_id':review_id
    };
    let url = getWebAppBackendUrl('/get_tweets_table')+'/'+JSON.stringify(params);
    let promise = fetch(url, init) 
                   .then(function(response) {
                       
                   }
                        )
}

$(document).ready(function(){
    let test = document.getElementById("bar-chart-group")
    console.log("test is ", test)
})


let tbl_pos = document.getElementById("insert_table_pos");
console.log("tbl_pos.rows.length", tbl_pos.rows.length)
if (tbl_pos != null) {
    for (let i = 0; i < tbl_pos.rows.length; i++) {
        for (let j = 0; j < tbl_pos.rows[i].cells.length; j++) {
            tbl_pos.rows[i].cells[j].onclick = (function (i, j) {
                return function () {
                    alert('R' + (i + 1) + 'C' + (j + 1));
                };
            }(i, j));
        }
    }
}

function modifyText() {
  const row_0 = document.getElementById("rowID_0");
  alert("clicked" + row_0.value)
}

// Add event listener to table
const el = document.getElementById("insert_table_pos");
el.addEventListener("click", modifyText, false);
*/

function addRowHandlers(data) {
    console.log("data looks like", data)
    var table = document.getElementById("insert_table_pos");
    var rows = table.getElementsByTagName("tr");
    console.log("until here it's good")
    for (i = 0; i < rows.length; i++) {
        console.log("row is", i)
        row = table.rows[i];
        row.onclick = function(){
            var cell = this.getElementsByTagName("td")[0];
            var topic = cell.innerHTML;
            console.log("clicked topic", topic);
            console.log("clicked row", row)
            
            let headers = new Headers();
            let init = {
                method : 'GET',
                headers : headers
            };
            let params = {
                'company':company,
                'category':category,
                'review_id':review_id
            };
            let url = getWebAppBackendUrl('/get_tweets_table')+'/'+JSON.stringify(params);

                      };
    }
}

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
    return $("#" + id).val();
}


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
    document.getElementById(id).innerHTML = '';
    i = 0
    Object.keys(itemJson).forEach(function(key) {
        // this iterates over rows
        // console.table('Key : ' + key + ', Value : ' + itemJson[key]);
        let topics = itemJson[key]["topics"]
        let averageScores = itemJson[key]["average scores"]
        let importanceScores = itemJson[key]["importance scores"]
        // console.log("topics", topics)
        // console.log("averageScores", averageScores)
        // console.log("importanceScores", importanceScores)
        let tbl = document.getElementById(id)        
        let row = tbl.insertRow(i)
        row.id = "rowID_" + i;
        let cell1 = row.insertCell(0);
        let cell2 = row.insertCell(1);
        let cell3 = row.insertCell(2);
        cell1.innerHTML = topics;
        cell2.innerHTML = averageScores;
        cell3.innerHTML = importanceScores;
        i += 1
        console.log("tbl.rows.length", tbl.rows.length)
})
    var orderArrayHeader = ["Topics", "Average scores","Importance scores"];
    var thead = document.createElement('thead');
    let finishedTable = document.getElementById(id)   
    finishedTable.appendChild(thead);
    for(var j=0;j<orderArrayHeader.length;j++){
        thead.appendChild(document.createElement("th")).
        appendChild(document.createTextNode(orderArrayHeader[j]));
    }
    
    let tblToClick = document.getElementById(id);
    for (let i = 0; i < tblToClick.rows.length; i++) {
        for (let j = 0; j < tblToClick.rows[i].cells.length; j++) {
            tblToClick.rows[i].cells[j].onclick = (function (i, j) {
                return function () {
                    // alert('R' + (i + 1) + 'C' + (j + 1));
                };
            }(i, j));
        }
    }
}

function addOptions(id, itemList){
    /* function to add company choice to the dropdowns */
    itemList.forEach(function(value, index){
        let option = document.createElement('option');
        option.text = value;
        document.getElementById(id).appendChild(option)
    })
}

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