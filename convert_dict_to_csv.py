import pandas as pd
import numpy as np
import pickle
import re

filename = "jobsdico.p"
jobsdico = pickle.load(open(filename, 'rb'))

clean_jobs_dico = {}
for k,v in jobsdico.items():
    joblocation = v["formattedLocation"]
    jobtitle = v["title"]
    jobofferdate = v["listedAt"]
    jobdescription = v["description"]["text"]
    resume = {"joblocation":joblocation,
              "jobtitle":jobtitle,
              "jobofferdate":jobofferdate,
              "jobdescription":jobdescription }
    clean_jobs_dico[k] = resume



jobid_compagany_dic = {}
errors = 0
for k,v in jobsdico.items():

    try:
        if "com.linkedin.voyager.deco.jobs.web.shared.WebCompactJobPostingCompany" in v["companyDetails"]:
            companyid = v["companyDetails"]["com.linkedin.voyager.deco.jobs.web.shared.WebCompactJobPostingCompany"]["companyResolutionResult"]["entityUrn"]
            companyid = re.findall(":[0-9]+$", companyid)[0]
            companyid = companyid[1:]
            companyname = v["companyDetails"]["com.linkedin.voyager.deco.jobs.web.shared.WebCompactJobPostingCompany"]["companyResolutionResult"]["name"]

        else:
            companyid = "UNKNOWN"
            companyname = v["companyDetails"]["com.linkedin.voyager.jobs.JobPostingCompanyName"]["companyName"]

    except:
        companyid ="UNKNOWN"
        companyname = "UNKNOWN"
        errors =errors + 1
        
    jobid_compagany_dic[k] = {"companyid" : companyid,"companyname" : companyname}





finaldicojob={}
for k,v in clean_jobs_dico.items():
    finaldicojob[k] = {"joblocation":v["joblocation"],
                       "jobtitle":v["jobtitle"],
                       "jobofferdate":v["jobofferdate"],
                       "jobdescription":v["jobdescription"],
                       "companyid" : jobid_compagany_dic[k]["companyid"],
                       "companyname" : jobid_compagany_dic[k]["companyname"]}


df = pd.DataFrame.from_dict(finaldicojob, orient="index")
filename = "job_offers.csv"
df.to_csv(filename,sep="\t")