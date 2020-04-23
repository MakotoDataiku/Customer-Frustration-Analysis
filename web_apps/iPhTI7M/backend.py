import dataiku
import pandas as pd
import json
import dataiku
import subprocess
from flask import send_file
from dataiku.scenario import Scenario

# To Edit:
OUTPUT_DATASET = "Cat_analysis_by_companies"
SCENARIO_ID = 'scraping_tweets'

PROJECT_KEY = dataiku.get_custom_variables()["projectKey"]
client = dataiku.api_client()
p = client.get_project(PROJECT_KEY)


@app.route('/init')
def init():
    data = p.get_variables()["standard"]
    if len(data) == 0:
        error = "<a id='link_var' target='_blank' href='../../variables/'> \
                 <i class='icon-exclamation-sign'></i> \
                 You need to add project variables.</a>"
    else:
        error = ""
    if OUTPUT_DATASET not in [d["name"] for d in p.list_datasets()]:
        error += "<br> \
                     <i class='icon-exclamation-sign'></i> \
                     Dataset {} does not exist -> \
                     edit in python backend.".format(OUTPUT_DATASET)
    if SCENARIO_ID not in [d["id"] for d in p.list_scenarios()]:
        error += "<br> \
                 <a id='link_var' target='_blank' href='../../scenarios/'> \
                 <i class='icon-exclamation-sign'></i> \
                 You need to create a scenario to compute {} \
                 and edit the python backend. </a>".format(OUTPUT_DATASET)
    return json.dumps({"status": "ok", "data": data, "scenario": SCENARIO_ID,
                       "output": OUTPUT_DATASET, "error": error})


@app.route('/run_scenario/<path:params>')
def run_scenario(params):
    params = json.loads(params)
    # 1/ updates variables in project variables.
    variables = p.get_variables()
    variables["standard"] = params
    p.set_variables(variables)
    # 2/ Clean the dataset impacted by those variables.
    for var_name in params.keys():
        clear_var_impacted("${"+var_name+"}")
    # 3/ Run the scenario.
    scenar = p.get_scenario(SCENARIO_ID)
    try:
        scenar.run_and_wait()
        jobSucceed = True
    except:
        jobSucceed = False
    # 4/ Return the job status.
    last_run = scenar.get_last_runs()[0]
    details = last_run.get_details()
    status = details['scenarioRun']['result']['outcome']
    job_details = get_jobs_details(last_run)
    if jobSucceed:
        df = dataiku.Dataset(OUTPUT_DATASET).get_dataframe(limit=200)
        sample = df.to_html(classes=['table'], border=0, index_names=0,
                            max_rows=20, max_cols=8, na_rep="", index=False)
        link = '../../datasets/'+OUTPUT_DATASET+'/explore/'
        output = OUTPUT_DATASET
    else:
        sample = ""
        jobId0 = last_run.get_details()["stepRuns"][0]
        jobId = jobId0["additionalReportItems"][-1:][0]['jobId']
        link = '../../jobs/'+jobId+"/"
        output = "job error"
    return json.dumps({"status": status, "output": output,
                       "sample": sample, "link": link,
                       "job_details": job_details})


@app.route("/download")
def download():
    df = dataiku.Dataset(OUTPUT_DATASET).get_dataframe()
    return df.to_csv(index=False)


def get_jobs_details(l):
    j = l.get_details()["stepRuns"][0]["additionalReportItems"]
    job_list = [i["target"] for i in j]
    d_list = [i["datasetName"] for i in job_list if "datasetName" in i]
    job_list2 = [i["outcome"] for i in j]
    run_list = pd.DataFrame(zip(d_list, job_list2))
    run_list.columns = ["datasetName", "status"]
    mapper = {"SUCCESS": '<i class="icon-thumbs-up-alt"></i>',
              "WARNING": '<i class="icon-warning-sign"></i>',
              "FAILED": '<i class="icon-thumbs-down"></i>'}
    run_list["status"] = run_list.status.map(mapper)
    out = run_list.to_html(classes='table', border=0,
                           index=False, escape=0, header=0)
    out = out.replace("\n", "")
    return out


def clear_var_impacted(var_name):
    """ Clear the datasets where the recipe building it contains a ${variable}
    """
    variables = dataiku.get_custom_variables()
    dip = variables['dip.home']
    pK = variables["projectKey"]
    dip += "/config/projects/"+pK+"/recipes/"

    outputs = []
    p = subprocess.Popen(
                        "grep -l '" + var_name + "' " + dip + "/*",
                        shell=True,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.STDOUT
                        )
    for line in p.stdout.readlines():
        if not line.endswith("json\n"):
            print(line)
            with open(
                    dip + "/" + line.split("/")[-1:][0].split(".")[0]+".json"
                    ) as data_file:
                data = json.load(data_file)
                try:
                    for o in data["outputs"]["main"]["items"]:
                        outputs.append(o["ref"])
                except KeyError:
                    print("ignore:", line)

    retval = p.wait()

    # Clear outputs where the variable is used.
    client = dataiku.api_client()
    p = client.get_project(pK)
    for o in list(set(outputs)):
        d = p.get_dataset(o)
        d.clear()
        print (o, " cleared")
