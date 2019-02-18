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


# * * * * * * * * * * * * * * * 
which_slave = "esclave1" # refers to a key of slaves_dico. Allow user to choose a linkedin account to crawl
# * * * * * * * * * * * * * * * 
BIGPATH = "/home/osboxes/projects/linkedin_scrapper/" # The root folder of the application
chrome_path = "/home/osboxes/projects/linkedin_scrapper/driver/chromedriver" # The folder of the chrome driver
# * * * * * * * * * * * * * * * 
duree_journee_type = 3600*8 # Total crawl duration in seconds
duree_max_travail_continue = 60*90 # Crawl duration without a break
# sleep_dico sets limits of different kinda pause duration during the crawl in order to look human being
sleep_dico = {"pause" : {"min" :600 , "max" :30*60 },
"big" : {"min" : 30, "max" :60 },
"middle" : {"min" : 10, "max" : 45},
"short" : {"min" : 5, "max" : 15}}
# slaves_dico sets parameters for differents linkedin accounts
slaves_dico = {"esclave1" : {"userid" : "jean-louis@gmail.com",
"password" : "****",
"query" : "https://www.linkedin.com/jobs/search/?f_E=3%2C4&f_TP=1&keywords=Machine%20Learning&location=Monde%20entier&locationId=OTHERS.worldwide"},
"esclave2" : {"userid" : "jean-paul@gmail.com",
"password" : "****",
"query" : "https://www.linkedin.com/jobs/search/?f_E=3%2C4&f_TP=1&keywords=Deep%20Learning&location=Monde%20entier&locationId=OTHERS.worldwide"}}
# * * * * * * * * * * * * * * * 
request_linkedin_job_offer = slaves_dico[which_slave]["query"]
scraping_name = "deeplearningmonde" # the name of the folder that will save scrapped data
working_folder =  scraping_name
the_date_prefix = time.strftime('%Y%m%d', time.localtime(int(time.time())))
jobidfilename = the_date_prefix + "_"+which_slave +"_jobsIDs.txt"
selected_steps = 4 # do not change
job_offer_saved = 0 # do not change
userid = slaves_dico[which_slave]["userid"]
password = slaves_dico[which_slave]["password"]
# * * * * * * * * * * * * * * *
