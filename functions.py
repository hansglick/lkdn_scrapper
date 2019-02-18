# Import libraries
from selenium import webdriver
from bs4 import BeautifulSoup
import getpass
import requests
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import pprint
import numpy as np
import time
import json
import re
import sys
import time
import os
import pickle
import unidecode


# Chope l'heure sous deux formats
def get_now():
	now_int = int(time.time())
	now_str = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(now_int))
	return now_int,now_str

# Chope l'objet elements d'une série de json
def extract_elements_object(my_jsons):
	for j in my_jsons:
		if "elements" in j["data"] and "metadata" in j["data"]:
			solution = j["data"]["elements"]
	return solution

# Chope les jobs id de l'objet élément 
def extract_jobids(elements_object):
	jobids_list = []
	for e in elements_object:
		rawjobid = e["hitInfo"]['jobPosting']
		jobid = re.findall(":[0-9]+$", rawjobid)[0]
		jobid = jobid[1:]
		jobids_list.append(jobid)
	return jobids_list

# Ecrit les job ids de la liste a la suite dans un fichier filename
def savejobids(filename,jobids):
	file = open(filename,"a") 
	for j in jobids:
		file.write(j+"\n")
	file.close()
	return None

# Ouvre et sauve un fichier du nom jobidfilename
def init_job_id_list(jobidfilename):
	file = open(jobidfilename,"w") 
	file.write("start" + "\n")
	file.close()
	return None

# Va sur linkedin et se connecte
def connect_to_linkedin(driver,userid,password):
	driver.get("https://www.linkedin.com")
	driver.implicitly_wait(20)
	driver.find_element_by_xpath("""//*[@id="login-email"]""").send_keys(userid)
	driver.find_element_by_xpath("""//*[@id="login-password"]""").send_keys(password)
	driver.find_element_by_xpath("""//*[@id="login-submit"]""").click()
	return None

# Pause le script pendant un instant
def generate_a_pause(sleep_dico,type_of_pause = "big"):

	if type_of_pause == "pause":
		duree = np.random.randint(sleep_dico["pause"]["min"],sleep_dico["pause"]["max"])

	if type_of_pause == "big":
		duree = np.random.randint(sleep_dico["big"]["min"],sleep_dico["big"]["max"]) #60,120

	if type_of_pause == "middle":
		duree = np.random.randint(sleep_dico["middle"]["min"],sleep_dico["middle"]["max"])#20,60

	if type_of_pause == "short":
		duree = np.random.randint(sleep_dico["short"]["min"],sleep_dico["short"]["max"])#10,20

	time.sleep(duree)

	return None

# Chope les jsons d'une page de job html
def extract_json_from_job_page(html_file):
	with open(html_file) as f:
		content = f.readlines()
	json_list = []
	for r in content:
		cleanrow = r.strip()
		if len(cleanrow)>10:
			if cleanrow[:9] == """{"company""":
				the_json= json.loads(cleanrow)
				json_list.append(the_json)
	return json_list

# Sauve la page présente en hmtl complete
def save_the_present_page(driver,filename):
	with open(filename, "w") as f:
		f.write(driver.page_source)
	return None

# Mime le comportement d'un homme lorsqu'il veut se rendre sur une page web
def reach_an_url(sleep_dico,driver,which_url):

	generate_a_pause(sleep_dico,type_of_pause = "big")
	driver.get(which_url)
	generate_a_pause(sleep_dico,type_of_pause = "middle")
	driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
	generate_a_pause(sleep_dico,type_of_pause = "short")

	return None

# Chope tout les jsons commencant par {data sur une page html
def extract_json_from_code_source(html_file):
	with open(html_file) as f:
		content = f.readlines()
	json_list = []
	for r in content:
		cleanrow = r.strip()
		if len(cleanrow)>10:
			if cleanrow[:6] == """{"data""":
				the_json= json.loads(cleanrow)
				json_list.append(the_json)
	return json_list

# Définit la navigation de la session
def shuffle_parcours_pages(pages,selected_steps):
    X = np.split(pages,np.arange(selected_steps,len(pages),selected_steps))
    for r in X:
        np.random.shuffle(r)
    X = np.concatenate(X)
    return X