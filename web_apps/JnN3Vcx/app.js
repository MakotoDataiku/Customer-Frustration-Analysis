setFilterOptions();

function setFilterOptions(){
    /* function to get distinct values of store id and product category and insert them in the dropdowns*/
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