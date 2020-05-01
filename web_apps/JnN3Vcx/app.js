setFilterOptions();

/* returns the company value chosen from the dropdowns */
document.getElementById('button').onclick = function(){
    let company = getSelectedOption('companies');
    let headers = new Headers()
    let init = {
        method : 'GET',
        headers : headers
    }
    let params = {
        'company':company
    }

    let url = getWebAppBackendUrl('/get_stats')+'/'+JSON.stringify(params)
    let promise = fetch(url, init) 
                   .then(function(response){ 
                       response.json()
                               .then(function(data){
                                addBarChart(data.chart);
                                })
                   });
    
}

function getSelectedOption(id){
    let select = document.getElementById(id);
    let value = select.options[select.selectedIndex].value;
    return value
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