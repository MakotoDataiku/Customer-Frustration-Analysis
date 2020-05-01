let default_colors = ['#FC427B','#16a085','#3498db','#9b59b6','#7ed6df','#3B3EAC','#0099C6','#DD4477','#66AA00','#B82E2E','#316395','#994499','#22AA99','#AAAA11','#6633CC','#E67300','#8B0707','#329262','#5574A6','#3B3EAC']
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
                                addBarChartJS(data.barChartJS.data, data.barChartJS.labels);
                                addBarChart(data.chart);
                                })
                   });
    
}

function getSelectedOption(id){
/* function to get the selected value from the dropdowns */
    let select = document.getElementById(id);
    let value = select.options[select.selectedIndex].value;
    console.log("selected comapny is ", value)
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

function addBarChartJS(data, labels) {
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

function addBarChart(data){
    document.getElementById('barChart').innerHTML = "";
    
    let width = 500;
    let height = 240;
    let margin = {
                top: 15,
                right: 55,
                bottom: 70,
                left: 60
            };
    
    let ymin = d3.min(data, function (d) {
                    return d.weighted_ave_tb});
    console.log("ymin is", ymin)
    
    let ymax = d3.max(data, function (d) {
                    return d.weighted_ave_tb});
    
    let xScale = d3.scale.ordinal()
          .domain(data.map(function(d){
              return d.group})
                 )
          .rangeBands([0, width],.1);

    let yScale = d3.scale.linear()
              .domain([ymin, ymax])
              .range([height, 0]);
    
    let xAxis = d3.svg.axis()
                  .scale(xScale)
                  .orient("bottom");
   
    let yAxis = d3.svg.axis()
                  .scale(yScale)
                  .orient("left")
                  .ticks(10);
    
    let svg = d3.select("#barChart")
                .append("svg")
                .attr("width", width + margin.left + margin.right)
                .attr("height", height + margin.top + margin.bottom)
    
    let g = svg.append("g")
       .attr("transform", "translate(" + margin.left + "," + margin.top + ")");
    
    g.append("g")
      .attr("class", "x axis")
      .attr("transform", "translate(0," + height + ")")
      .call(xAxis)
      .selectAll("text")
      .style("text-anchor", "end")
      .attr("dx", "-.8em")
      .attr("dy", "-.50em")
      .attr("transform", "rotate(-90)" );

   g.append("g")
      .attr("class", "y axis")
      .call(yAxis)
      .append("text")
      .attr("transform", "rotate(-90)")
      .attr("y", 6)
      .attr("dy", ".71em")
      .style("text-anchor", "end")
      .text("Sentiment score");

    let bar = g.selectAll("rect")
            .data(data)
            .enter()
            .append("rect")
            .attr("x", function (d) {
                return xScale(d.group);
            })        
            .attr("width", xScale.rangeBand())
            .attr("y", function(d) { return yScale(d.weighted_ave_tb); })
            .attr("height", function(d) { 
                return height - yScale(d.weighted_ave_tb); })
            .attr("fill","#01a3a4");
    
    let title = g.append("text")
        .attr("x", (width / 2))             
        .attr("y", 0 - margin.top / 3)
        .attr("text-anchor", "middle")  
        .style("font-size", "12px") 
        .text("Sentiment by category");

}