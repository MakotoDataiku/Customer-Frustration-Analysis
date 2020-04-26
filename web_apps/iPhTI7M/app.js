
function init() {
    var init_var = $.getJSON(getWebAppBackendUrl('init'), function(data){
        console.log("received from backend : ", data);
        d3.select("#init").text("Enter the parameters");
        var variables = data["data"];
        
        if (data["error"] != "") {
            d3.select("#error").html(data["error"]);
            d3.select("#init").html("ERROR");
        }
        else {
        
        // add a box to enter a parameter
        // iterates for each project parameter    
        Object.keys(variables).forEach(function(key,index) {
        
        box = d3.select("#variables").append("div")
                                     .attr("class","form-group");
            
        box.append("label")
           .attr("for",key)
           .text(key);
            
        box.append("input")
           .attr("type","text")
           .attr("class","form-control")
           .attr("id", key)
           .attr("value", variables[key]);
        });
        
        // add Run scenario button
        d3.select("#variables").append("button")
                               .attr("class","btn btn-primary")
                               .style("margin-top", "10px")
                               .style("margin-right", "10px")
                               .attr("id", "run_flow")
                               .html('<i class="icon-play"></i> Run scenario : ' + data["scenario"])
                               .attr("data-loading-text", "<i class='fa fa-circle-o-notch fa-spin'></i> Scenario running")
                               .on("click", run_scenario);
        
        // add download button
        d3.select("#variables").append("a")
                       .attr("id", "download_link")
                       .attr("download", data["output"] + ".csv")
                       .attr("href", getWebAppBackendUrl('download'));



        d3.select("#download_link").append("button")
                       .attr("class","btn btn-primary")
                       .style("margin-top", "10px")
                       .style("margin-right", "10px")
                       .attr("id", "download")
                       .html('<i class="icon-download-alt"></i> Download '+data["output"])
                       .on("click", download);

        }
    })
 }

function run_scenario() {
    
    var $this = $(this); //  = document.getElementById(this)
    $this.button('loading');

    /* Getting all the input into an object that we will pass to the backend as a parameter of the call*/
    variables = {};
    $('.form-control').each(function(index){
        variables[$(this).prop('id')] = $(this).val();
    });
    
    d3.select("#download").attr("class","btn btn-primary disabled");
    
    console.log("sending to backend : ", variables);
    
    var flow_run =$.getJSON(getWebAppBackendUrl('run_scenario')+'/'+JSON.stringify(variables),function(data){
        console.log(data);
        
        d3.select("#job_details").html(data["job_details"]);
        
        $this.button('reset');
        d3.selectAll(".btn").attr("class", function(d) {
            if (data["status"] == "SUCCESS") {return "btn btn-success"}
            else { return "btn btn-danger" }});
        
         d3.select("#run_flow").text(function(d) {
                                    if (data["status"] == "SUCCESS") {return "Scenario succeeded"}
                                    else { return "Scenario Failed" }});
        
       

        
        $('#df_table').append(data['sample'])
        $('#link_go_to').attr("href", data['link'])
              .text("Go to " + data["output"]);
        $('#df_table').show();
        $('#job_details').show();

        
     }) 
 }

function download() {
        var init_var = $.getJSON(getWebAppBackendUrl('download'),function(data){
                console.log("received from backend : ", data)
     })
 }


init();