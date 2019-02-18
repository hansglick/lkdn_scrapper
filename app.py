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
from functions import *
from conf import *


if not os.path.exists(BIGPATH + "jobsdico.p"):
	jobsdico = {}
	pickle.dump(jobsdico, open(BIGPATH + 'jobsdico.p', 'wb'))

print(get_now()[1] + " : " + "Charge la base de données des offres d'emplois", file=sys.stdout, flush=True)
jobsdico = pickle.load(open(BIGPATH + 'jobsdico.p', 'rb'))



print(get_now()[1] + " : " + "Define scrapping folder", file=sys.stdout, flush=True)
working_folder = scraping_name
if not os.path.exists(BIGPATH + working_folder):
	os.makedirs(BIGPATH + working_folder)




print(get_now()[1] + " : " + "Initialisation de la job id list", file=sys.stdout, flush=True)
init_job_id_list(BIGPATH + jobidfilename)



print(get_now()[1] + " : " + "Initialisation du driver Chrome", file=sys.stdout, flush=True)
driver = webdriver.Chrome(chrome_path)
driver.implicitly_wait(20)



print(get_now()[1] + " : " + "Connection à Linkedin", file=sys.stdout, flush=True)
connect_to_linkedin(driver,userid,password)
log_to_print = ",".join([str(i) for i in get_now()]) + ","+"connection to linkedin"
print(log_to_print, file=sys.stderr, flush=True)



print(get_now()[1] + " : " + "L'esclave scroll down son fil d'actualité", file=sys.stdout, flush=True)
generate_a_pause(sleep_dico,type_of_pause = "short")
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")



print(get_now()[1] + " : " + "Initialisation des variables mesurant le temps", file=sys.stdout, flush=True)
debut_de_journee = int(time.time())
debut_du_taff = int(time.time())



print(get_now()[1] + " : " + "Pause du robot", file=sys.stdout, flush=True)
generate_a_pause(sleep_dico,type_of_pause = "pause")



print(get_now()[1] + " : " + "Lance la recherche d'emplois", file=sys.stdout, flush=True)
reach_an_url(sleep_dico,driver,request_linkedin_job_offer)



print(get_now()[1] + " : " + "Sauve la page HTML en cours", file=sys.stdout, flush=True)
save_the_present_page(driver,filename = BIGPATH + working_folder + "/" + the_date_prefix + "_page_request_0.html")
log_to_print = ",".join([str(i) for i in get_now()]) + ","+"save html page_request_0"
print(log_to_print, file=sys.stderr, flush=True)



print(get_now()[1] + " : " + "Recherche le nombre d'offres de disponible", file=sys.stdout, flush=True)
soup = BeautifulSoup(open(BIGPATH + working_folder + "/" + the_date_prefix + "_page_request_0.html"), "html.parser")
n_jobs_offers_request = soup.find_all('div', attrs={"class":"t-12 t-black--light t-normal"})
n_jobs_offers = n_jobs_offers_request[0].text.split(" ")[0]
n_jobs_offers = unidecode.unidecode(n_jobs_offers)
n_jobs_offers = int(n_jobs_offers.replace(" ", ""))


print(get_now()[1] + " : " + "Il existe " + str(n_jobs_offers) + " offres d'emplois", file=sys.stdout, flush=True)
log_to_print = ",".join([str(i) for i in get_now()]) + ","+"extract number of job offers"
print(log_to_print, file=sys.stderr, flush=True)



print(get_now()[1] + " : " + "Définition du parcours des pages de recherches de la session", file=sys.stdout, flush=True)
pages_restantes = np.arange(25,n_jobs_offers+1,25)
pages_restantes = np.insert(pages_restantes,0,0)
pages_restantes = shuffle_parcours_pages(pages_restantes,selected_steps)
print(get_now()[1] + " : " + "Parcours choisi : " + " | ".join([str(i) for i in pages_restantes]), file=sys.stdout, flush=True)
security_check = 0

print("")
for idx_which_page,which_page in enumerate(pages_restantes):

	# security check
	security_check = security_check + 1
	# if security_check>4:
	#	break
	# Controle de la journée du bot si ca fait trop longtemps alors il arrete
	duree_journee = int(time.time()) - debut_de_journee
	print(get_now()[1] + " : " + "L'esclave travaille depuis " + str(int(duree_journee/60)) + " minutes", file=sys.stdout, flush=True)
	if duree_journee>duree_journee_type:
		print(get_now()[1] + " : " + "L'esclave travaille depuis trop longtemps, journée terminée!", file=sys.stdout, flush=True)
		log_to_print = ",".join([str(i) for i in get_now()]) + ", journée terminée!"
		print(log_to_print, file=sys.stderr, flush=True)
		break


	# Va sur une page de recherche
	if which_page == 0:
		which_url = request_linkedin_job_offer
	else:
		which_url = request_linkedin_job_offer + "&start=" + str(which_page)
	print(get_now()[1] + " : " + "Accède à la page de recherche n°" + str(which_page) + " ("+ str(idx_which_page+1)+"/"+str(len(pages_restantes)) +")", file=sys.stdout, flush=True)
	reach_an_url(sleep_dico,driver,which_url)
	log_to_print = ",".join([str(i) for i in get_now()]) + ","+"boucle A - " + "reach url:" + which_url
	print(log_to_print, file=sys.stderr, flush=True)


	#Sauve la page en cours au format HTML
	print(get_now()[1] + " : " + "Sauve la page de recherche en cours au format HTML", file=sys.stdout, flush=True)
	save_the_present_page(driver,filename = BIGPATH + working_folder + "/" + the_date_prefix + "_page_request_" + str(which_page) + ".html")
	log_to_print = ",".join([str(i) for i in get_now()]) + ","+"boucle A - " + "save page:" + "page_request_" + str(which_page) + ".html"
	print(log_to_print, file=sys.stderr, flush=True)


	# Processus afin de récupérer les jobs IDs de la page de recherche
	print(get_now()[1] + " : " + "Extrait les JSONS inclus dans la page en cours", file=sys.stdout, flush=True)
	my_jsons = extract_json_from_code_source(BIGPATH + working_folder + "/" + the_date_prefix + "_page_request_" + str(which_page) + ".html")
	log_to_print = ",".join([str(i) for i in get_now()]) + ","+"boucle A - " + "extract jsons from:" + which_url
	print(log_to_print, file=sys.stderr, flush=True)
	
	print(get_now()[1] + " : " + "Recherche l'objet ELEMENT parmi les JSONs extraits", file=sys.stdout, flush=True)
	elements_object = extract_elements_object(my_jsons)
	log_to_print = ",".join([str(i) for i in get_now()]) + ","+"boucle A - " + "extract element object from:" + which_url
	print(log_to_print, file=sys.stderr, flush=True)

	print(get_now()[1] + " : " + "Extraction des Jobs IDs présents sur la page en cours", file=sys.stdout, flush=True)
	jobids = extract_jobids(elements_object)
	log_to_print = ",".join([str(i) for i in get_now()]) + ","+"boucle A - " + "extract jobs ids from:" + which_url
	print(log_to_print, file=sys.stderr, flush=True)

	print(get_now()[1] + " : " + "Sauvegarde des JSONs sur le disque", file=sys.stdout, flush=True)
	savejobids(jobidfilename,jobids)
	for idjson,ajson in enumerate(my_jsons):
		with open(BIGPATH + working_folder + "/" + the_date_prefix + "_" +which_slave +"_json_"+str(idjson)+"_page_"+str(which_page)+".json", 'w') as fp:
			json.dump(ajson,
					  fp,
					  indent=5)

	# Print les informations extraites des JSONs de la page de recherche
	jobids_restants = np.array(jobids)
	print(get_now()[1] + " : " + "Nombre de jobs IDs dans la page de recherche en cours : " + str(len(jobids_restants)), file=sys.stdout, flush=True)
	already_saved_jobs_ids = np.array(list(jobsdico.keys()))
	print(get_now()[1] + " : " + "Nombre de jobs IDs recensés dans la base de données : " + str(len(already_saved_jobs_ids)), file=sys.stdout, flush=True)
	jobids_dejavu = np.intersect1d(jobids_restants,already_saved_jobs_ids)
	jobids_restants = np.setdiff1d(jobids_restants,already_saved_jobs_ids)
	print(get_now()[1] + " : " + "Nombre de jobs IDs présents sur la page en cours et absent de la bdd : " + str(len(jobids_restants)), file=sys.stdout, flush=True)



	# Génération de la rigueur de l'esclave
	skill_esclave = np.random.choice(np.array(["rigoureux","brouillon"]),size = 1, p =np.array([0.5,0.5]))[0]
	if skill_esclave == "brouillon" and len(jobids_dejavu)>0:
		jobids_restants = np.append(jobids_restants,jobids_dejavu[0])
		job_offer_saved = job_offer_saved - 1
		print(get_now()[1] + " : " + "L'esclave est n'est qu'un homme, il va parcourir une offre qu'il a déjà vu", file=sys.stdout, flush=True)



	print(get_now()[1] + " : " + "Définition de la navigation de l'esclave pour les jobs IDs de la page de recherche en cours", file=sys.stdout, flush=True)
	np.random.shuffle(jobids_restants)
	security_check_bis = 0

	print("")

	

	for idx_which_job,which_job in enumerate(jobids_restants):

		# Security check
		security_check_bis = security_check_bis + 1
		# if security_check_bis>3:
		#	break


		
		print(get_now()[1] + " : " + "Visite de la job ID " + str(which_job) + " ("+ str(idx_which_job+1)+"/"+str(len(jobids_restants)) +")", file=sys.stdout, flush=True)
		which_url = "https://www.linkedin.com/jobs/view/" + str(which_job)
		reach_an_url(sleep_dico,driver,which_url)
		log_to_print = ",".join([str(i) for i in get_now()]) + ","+"boucle B - " + "reach url:" + which_url
		print(log_to_print, file=sys.stderr, flush=True)

		

		print(get_now()[1] + " : " + "Enregistre la fiche de poste en cours (" + str(which_job) + ")", file=sys.stdout, flush=True)
		save_the_present_page(driver,filename = BIGPATH + working_folder + "/" + the_date_prefix + "_page_job_" + str(which_job) + ".html")
		log_to_print = ",".join([str(i) for i in get_now()]) + ","+"boucle B - " + "save page:" + "page_job_" + str(which_job) + ".html"
		print(log_to_print, file=sys.stderr, flush=True)

		

		print(get_now()[1] + " : " + "Extrait et sauve le json de la job ID (" + str(which_job) + ")", file=sys.stdout, flush=True)
		jsonjobofferlist = extract_json_from_job_page(BIGPATH + working_folder + "/" + the_date_prefix + "_page_job_" + str(which_job) + ".html")
		if len(jsonjobofferlist)==0:
			print(get_now()[1] + " : " + "L'esclave n'a pas trouvé de JSON correspondant", file=sys.stdout, flush=True)
			break
		jsonjoboffer = jsonjobofferlist[0]
		jobsdico[which_job] = jsonjoboffer
		pickle.dump(jobsdico, open(BIGPATH + 'jobsdico.p', 'wb'))
		jobsdico = pickle.load(open(BIGPATH + 'jobsdico.p', 'rb'))
		print(get_now()[1] + " : " + "Il y a actuellement " + str(len(jobsdico)) + " fiches de postes recensées dans la base", file=sys.stdout, flush=True)
		log_to_print = ",".join([str(i) for i in get_now()]) + ","+"boucle B - " + "save json job offer in db:" + str(which_job)
		print(log_to_print, file=sys.stderr, flush=True)



		# Calcul du nombre d'offres d'emplois enregistrées depuis le début de la session
		job_offer_saved = job_offer_saved + 1
		travail_continue = int(time.time()) - debut_de_journee
		vitesse_job_saved = round((job_offer_saved / (travail_continue/3600)) , 1)
		print(get_now()[1] + " : " + "L'esclave a enregistré " + str(job_offer_saved) + " offres d'emplois depuis le début de la session (" + str(vitesse_job_saved) + " j/h)", file=sys.stdout, flush=True)



		# On verifie si ca fait pas trop longtemps qu il bosse
		travail_continue = int(time.time()) - debut_du_taff
		print(get_now()[1] + " : " + "L'esclave a travaillé " + str(int(travail_continue/60)) + " minutes depuis sa dernière pause", file=sys.stdout, flush=True)
		if travail_continue>duree_max_travail_continue:
			print(get_now()[1] + " : " + "En conséquence, l'esclave prend sa pause", file=sys.stdout, flush=True)
			log_to_print = ",".join([str(i) for i in get_now()]) + ","+"en pause"
			print(log_to_print, file=sys.stderr, flush=True)
			generate_a_pause(sleep_dico,type_of_pause = "pause")
			debut_du_taff = int(time.time())

		print("")





pickle.dump(jobsdico, open(BIGPATH + 'jobsdico.p', 'wb'))