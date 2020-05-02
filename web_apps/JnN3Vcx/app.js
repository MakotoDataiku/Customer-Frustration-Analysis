let default_colors = ['#FC427B','#16a085','#3498db','#9b59b6','#7ed6df','#3B3EAC','#0099C6','#DD4477','#66AA00','#B82E2E','#316395','#994499','#22AA99','#AAAA11','#6633CC','#E67300','#8B0707','#329262','#5574A6','#3B3EAC']
setFilterOptions();

console.log($(document).ready(function() { 
 $("#companies").select2();
}))

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
                                addBarChart(data.chart.data, data.chart.labels);
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


function getSelectedOption(id){
    
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

function addOptions(id, itemList){
    /* function to add company choice to the dropdowns */
    itemList.forEach(function(value, index){
        let option = document.createElement('option');
        option.text = value;
        document.getElementById(id).appendChild(option)
    })
}



function addBarChart(data, labels) {
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

function addGroupBarChart(data, labels) {
    document.getElementById('table_stats').innerHTML = '<canvas id="bar-chart-group" ></canvas>';
    let data = {
        labels: labels,
        datasets: [
            {
                label: "Blue",
                backgroundColor: "blue",
                data: [3,7,4]
            },
            {
                label: "Red",
                backgroundColor: "red",
                data: [4,3,5]
            },
            {
                label: "Green",
                backgroundColor: "green",
                data: [7,2,6]
            }
        ]
    };
    new Chart(document.getElementById("bar-chart-group"), {
        type: "bar",
        
        data: data,
        options: {
          title: {
            display: false,
            text: "Sentiment by category"
          },
          scales: {
          yAxes: [{
              ticks: {
                  min: 0,
              }
          }]
      }
        }
    });
}