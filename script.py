from bs4 import BeautifulSoup
import requests
import smtplib
from email.message import EmailMessage
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
import os
EMAIL = "XXXXX"
PASSWORD = "XXXXX" 
def sendMail(pp,reciever,wantFile):
	msg = EmailMessage()
	msg['Subject'] = 'Store Invintory'
	msg['From'] = EMAIL
	msg['To'] = reciever
	msg.set_content(pp)


	with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
		smtp.login(EMAIL,PASSWORD)
		with open (wantFile, 'rb') as f:
			file_data = f.read()
			file_name = f.name
		msg.add_attachment(file_data, maintype = 'text', subtype = 'txt', filename = file_name)
	
		smtp.send_message(msg)
def sendMail2(pp,reciever,wantFile,wantFile2):
	msg = EmailMessage()
	msg['Subject'] = 'Store Invintory'
	msg['From'] = EMAIL
	msg['To'] = reciever
	msg.set_content(pp)


	with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
		smtp.login(EMAIL,PASSWORD)
		with open (wantFile, 'rb') as f:
			file_data = f.read()
			file_name = f.name
		msg.add_attachment(file_data, maintype = 'text', subtype = 'txt', filename = file_name)
		with open (wantFile2, 'rb') as f:
			file_data = f.read()
			file_name = f.name
		msg.add_attachment(file_data, maintype = 'text', subtype = 'txt', filename = file_name)
		smtp.send_message(msg)		

def walmartupdateZip(link,driver):
	try:
		zipCodeNum = '08873'
		zipCode = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div[1]/div/div[1]/div/div[5]/div[1]/div[3]/button")))
		zipCode = driver.find_element_by_xpath("/html/body/div[1]/div[1]/div/div[1]/div/div[5]/div[1]/div[3]/button").click()
		print("Clicked ZipCode")
		zipCode = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div/div/div[1]/div/div[4]/div[1]/div/div[2]/div[1]/div/div[1]/input")))
		zipCode = driver.find_element_by_xpath("/html/body/div[1]/div/div/div[1]/div/div[4]/div[1]/div/div[2]/div[1]/div/div[1]/input")

		zipCode.click()
		zipCode.send_keys(zipCodeNum)
		print("Entered ZipCode")
		zipCode.send_keys(Keys.RETURN)
		print("Successfully Updated ZipCode:")
		driver.refresh()
	except TimeoutException:
		print("Page Didnt Load...Reloading")
		driver.get(link)
		return walmartupdateZip(link,driver)
def walmartgetName(driver,link):
	try:
		name = WebDriverWait(driver, 0).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div[1]/div/div[2]/div/div[1]/div/div[1]/div/div/div/div/div[3]/div[5]/div/div[3]/div/h1")))
		name = driver.find_element_by_xpath("/html/body/div[1]/div[1]/div/div[2]/div/div[1]/div/div[1]/div/div/div/div/div[3]/div[5]/div/div[3]/div/h1")

		return (name.text)
	except TimeoutException:
		print("Page Didnt Load...Reloading")
		driver.get(link)
		return getName(driver,link)
def walmartgetPrice(driver,link):
	try:
		price = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div[1]/div/div[2]/div/div[1]/div/div[1]/div/div/div/div/div[3]/div[5]/div/div[3]/div/div[2]/div[1]/section/div/div[1]/div[1]/span/div/span[1]/span/span[1]")))
		price = driver.find_element_by_xpath("/html/body/div[1]/div[1]/div/div[2]/div/div[1]/div/div[1]/div/div/div/div/div[3]/div[5]/div/div[3]/div/div[2]/div[1]/section/div/div[1]/div[1]/span/div/span[1]/span/span[1]")
		return (price.text)
	except TimeoutException:
		return "Cant Grab Price"
def walmartgetStock(driver):
	try:
		stock = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div[1]/div/div[2]/div/div[1]/div/div[1]/div/div/div/div/div[3]/div[5]/div/div[3]/div/div[2]/div[1]/section/div/div[2]")))
		stock = driver.find_element_by_xpath("/html/body/div[1]/div[1]/div/div[2]/div/div[1]/div/div[1]/div/div/div/div/div[3]/div[5]/div/div[3]/div/div[2]/div[1]/section/div/div[2]")
		if "out of stock" in stock.text.lower():
			return (stock.text.upper())
		else:
			fianlText = "Cant Read Check Site"
			invintory = driver.find_element_by_xpath("/html/body/div[1]/div[1]/div/div[2]/div/div[1]/div/div[1]/div/div/div/div/div[3]/div[5]/div/div[3]/div/div[2]/div[2]")
			stock = driver.find_elements_by_xpath('//div[@class="prod-fulfillment"]')
			for instore in stock:
				if ("Free pickup today" in instore.text) or ("Price for in-store purchase only" in instore.text):
					if "Free pickup today" in instore.text:
						fianlText = instore.text.replace("Free pickup today","")
					if "Price for in-store purchase only" in instore.text:
						fianlText = instore.text.replace("Price for in-store purchase only","")
					fianlText = fianlText.replace("\n","")
				return(fianlText)

	except TimeoutException:
		fianlText = "Cant Read Check Site"
		invintory = driver.find_element_by_xpath("/html/body/div[1]/div[1]/div/div[2]/div/div[1]/div/div[1]/div/div/div/div/div[3]/div[5]/div/div[3]/div/div[2]/div[2]")
		stock = driver.find_elements_by_xpath('//div[@class="prod-fulfillment"]')
		for instore in stock:
			if ("Free pickup today" in instore.text) or ("Price for in-store purchase only" in instore.text):
				if "Free pickup today" in instore.text:
					fianlText = instore.text.replace("Free pickup today","")
				if "Price for in-store purchase only" in instore.text:
					fianlText = instore.text.replace("Price for in-store purchase only","")
				fianlText = fianlText.replace("\n","")
			return(fianlText)
def walmartItems(file,link):
	print(link)
	source = requests.get(link).text
	soup = BeautifulSoup(source, 'lxml')
	#print(soup.prittify())
	grid = soup.find(attrs={"data-automation-id": "search-result-gridview-items"})
	value = 0
	item = grid.find(attrs={"data-tl-id":"ProductTileGridView-0"})
	driver = webdriver.Chrome()
	driver.get('https://www.walmart.com/')
	walmartupdateZip('https://www.walmart.com/',driver)
	while item != None:
		internalLinks = item.find('a')
		links = (internalLinks.get('href'))
		driver.get('https://walmart.com/' + links)
		totals = "\n\tName Of Product: " + walmartgetName(driver,links) + "\n\n\t\t" + "Price: " + walmartgetPrice(driver,links) + "\n\t\t" + "Status: " + walmartgetStock(driver) + "\n\t\t" + "Link: " + 'https://walmart.com/' + links +"\n"
		#print(totals)
		file.write(totals)
		value = value + 1
		item = grid.find(attrs={"data-tl-id":"ProductTileGridView-" + str(value)})
	driver.quit()

def homedepotgetStock(driver):
	try:
		earlyDate = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[4]/div[3]/div/div/div[2]/div[2]/div[2]/div[6]/form")))
		earlyDate = driver.find_element_by_xpath("/html/body/div[4]/div[3]/div/div/div[2]/div[2]/div[2]/div[6]/form")
		earlyDate = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[4]/div[3]/div/div/div[2]/div[2]/div[2]/div[6]/form/span/input")))
		earlyDate = driver.find_element_by_xpath("/html/body/div[4]/div[3]/div/div/div[2]/div[2]/div[2]/div[6]/form/span/input")
		earlyDate.click()
		earlyDate.send_keys('08873')
		earlyDate.send_keys(Keys.RETURN)
		earlyDate = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[4]/div[3]/div/div/div[2]/div[2]/div[2]/div[6]/div/span")))
		earlyDate = driver.find_element_by_xpath("/html/body/div[4]/div[3]/div/div/div[2]/div[2]/div[2]/div[6]/div/span")
		return earlyDate.text
	except TimeoutException:
		try:
			stock = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[4]/div[3]/div/div/div[2]/div[2]/div[2]/div[8]/div/div/a/span")))
			stock = driver.find_element_by_xpath("/html/body/div[4]/div[3]/div/div/div[2]/div[2]/div[2]/div[8]/div/div/a/span")
			return("In Stock: " + stock.text)

		except TimeoutException:
			return("Out of Stock Check Website")
def homeDepotPrice(driver,link):
	try:
		price = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[4]/div[3]/div/div/div[2]/div[2]/div[2]/div[2]/div[1]/div[1]/span/span[2]")))
		price = driver.find_element_by_xpath("/html/body/div[4]/div[3]/div/div/div[2]/div[2]/div[2]/div[2]/div[1]/div[1]/span/span[2]")
		#cents = driver.find_elements_by_xpath("/html/body/div[4]/div[3]/div/div/div[2]/div[2]/div[2]/div[2]/div[1]/div[1]/span/span[3]")
		return ("$" + price.text)
	except TimeoutException:
		#driver.get(link)
		return ("Cant Grab Price Check Link")		#driver.get(link)
def homeDepotupdateZip(driver):
	try:
		zipCodeNum = '08873'
		zipCode = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div[2]/div[1]/div[2]/div[1]/div/div[3]/div[1]/a/span[2]/div[1]")))
		zipCode = driver.find_element_by_xpath("/html/body/div[1]/div[2]/div[1]/div[2]/div[1]/div/div[3]/div[1]/a/span[2]/div[1]").click()
		print("Clicked ZipCode")
		zipCode = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[13]/div[2]/div/div/div/div[4]/a")))
		zipCode = driver.find_element_by_xpath("/html/body/div[13]/div[2]/div/div/div/div[4]/a")
		zipCode.click()
		print('Clicked Find Other Stores')
		zipCode = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div[2]/div[2]/div/div/div[1]/div[2]/form/input")))
		zipCode = driver.find_element_by_xpath("/html/body/div[1]/div[2]/div[2]/div/div/div[1]/div[2]/form/input")
		zipCode.click()
		zipCode.send_keys(zipCodeNum)
		zipCode.send_keys(Keys.RETURN)
		print("Entered ZipCode")
		zipCode = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div[2]/div[2]/div/div/div[2]/div[1]/div[6]/button")))
		zipCode = driver.find_element_by_xpath("/html/body/div[1]/div[2]/div[2]/div/div/div[2]/div[1]/div[6]/button")
		zipCode.click()
		print("Updated Store Location")
		print("Successfully Updated ZipCode:")
		driver.refresh()	
	except:
		print("Couldnt Load Page refreshing...")
		driver.refresh()
		homeDepotupdateZip(driver)
def homeDepotName(driver,link):
	try:
		name = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[4]/div[3]/div/div/div[2]/div[2]/div[1]/h1")))
		name = driver.find_element_by_xpath("/html/body/div[4]/div[3]/div/div/div[2]/div[2]/div[1]/h1")
		return (name.text)
	except TimeoutException:
		print("Page Didnt Load Cant Get Name...Reloading")
		driver.get(link)
		return homeDepotName(driver,link)
def homeDepotItems(file,link):
	ua = UserAgent()
	header = {'User-Agent':str(ua.random)}
	soruce = requests.get(link,headers = header).text
	soup = BeautifulSoup(soruce, 'lxml')
	grid = soup.find(attrs={"data-section": "gridview"})
	value = 0
	item = grid.find(attrs={"data-pos":"0"})
	driver = webdriver.Chrome()
	driver.get('https://www.homedepot.com/')
	homeDepotupdateZip(driver)
	while item != None:
		internalLinks = item.find('a')
		links = (internalLinks.get('href'))
		driver.get('https://www.homedepot.com/' + links)
		totals = "\n\tName Of Product: " + homeDepotName(driver,links) + "\n\n\t\t" + "Price: " + homeDepotPrice(driver,links) + "\n\t\t" + "Status: " + homedepotgetStock(driver) + "\n\t\t" + "Item Link: " + 'https://www.homedepot.com/' + links +"\n"
		#print(totals)
		file.write(totals)
		value = value + 1
		item = grid.find(attrs={"data-pos":str(value)})
	driver.quit()

def lowesgetStock(driver):
	try:
		stock = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/section/div/div[4]/form/div[2]/button[1]")))
		stock = driver.find_element_by_xpath("/html/body/div[1]/section/div/div[4]/form/div[2]/button[1]")
		if "add to cart" in stock.text.lower():
			return ("In Stock")
		else:
			return(stock.text)
		
			#stock = driver.find_elements_by_xpath('//div[@class="prod-fulfillment"]')
			# for instore in invintory:
			# 	# if ("Free pickup today" in instore.text) or ("Price for in-store purchase only" in instore.text):
			# 	# 	if "Free pickup today" in instore.text:
			# 	# 		fianlText = instore.text.replace("Free pickup today","")
			# 	# 	if "Price for in-store purchase only" in instore.text:
			# 	# 		fianlText = instore.text.replace("Price for in-store purchase only","")
			# 	# 	fianlText = fianlText.replace("\n","")
			# 	return(instore)

	except TimeoutException:
		return("Out of Stock Check Website")

		# fianlText = "Cant Read Check Site"
		# invintory = driver.find_element_by_xpath("/html/body/div[1]/div[1]/div/div[2]/div/div[1]/div/div[1]/div/div/div/div/div[3]/div[5]/div/div[3]/div/div[2]/div[2]")
		# stock = driver.find_elements_by_xpath('//div[@class="prod-fulfillment"]')
		# for instore in stock:
		# 	if ("Free pickup today" in instore.text) or ("Price for in-store purchase only" in instore.text):
		# 		if "Free pickup today" in instore.text:
		# 			fianlText = instore.text.replace("Free pickup today","")
		# 		if "Price for in-store purchase only" in instore.text:
		# 			fianlText = instore.text.replace("Price for in-store purchase only","")
		# 		fianlText = fianlText.replace("\n","")
def lowesPrice(driver,link):
	try:
		price = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/section/div/div[4]/div[1]/div[1]/div[1]/span/span")))
		price = driver.find_element_by_xpath("/html/body/div[1]/section/div/div[4]/div[1]/div[1]/div[1]/span/span")
		#cents = driver.find_elements_by_xpath("/html/body/div[4]/div[3]/div/div/div[2]/div[2]/div[2]/div[2]/div[1]/div[1]/span/span[3]")
		return (price.text)
	except TimeoutException:
		#driver.get(link)
		return ("Cant Grab Price Check Link")		#driver.get(link)
def lowesName(driver,link):
	try:
		name = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/section/div/div[4]/div[1]/div[2]/h1")))
		name = driver.find_element_by_xpath("/html/body/div[1]/section/div/div[4]/div[1]/div[2]/h1")
		return (name.text)
	except TimeoutException:
		print("Page Didnt Load Cant Get Name...Reloading")
		driver.get(link)
		return lowesName(driver,link)
def lowesupdateZip(driver):
	try:
		zipCodeNum = '08873'
		zipCode = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div/div[2]/header/div[2]/div[1]/div/div/div/div[2]/div[1]/a/div")))
		zipCode = driver.find_element_by_xpath("/html/body/div[1]/div/div[2]/header/div[2]/div[1]/div/div/div/div[2]/div[1]/a/div").click()
		print("Clicked ZipCode")
		# zipCode = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[13]/div[2]/div/div/div/div[4]/a")))
		# zipCode = driver.find_element_by_xpath("/html/body/div[13]/div[2]/div/div/div/div[4]/a")
		# zipCode.click()
		# print('Clicked Find Other Stores')
		zipCode = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div/div[4]/div[2]/div/div[1]/div/form/div/div/input")))
		zipCode = driver.find_element_by_xpath("/html/body/div[1]/div/div[4]/div[2]/div/div[1]/div/form/div/div/input")
		zipCode.click()
		zipCode.send_keys(zipCodeNum)
		zipCode.send_keys(Keys.RETURN)
		print("Entered ZipCode")
		zipCode = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div/div[4]/div[2]/div/div[2]/div[1]/div/ul/li[1]/div/div[2]/button")))
		zipCode = driver.find_element_by_xpath("/html/body/div[1]/div/div[4]/div[2]/div/div[2]/div[1]/div/ul/li[1]/div/div[2]/button")
		zipCode.click()
		print("Updated Store Location")
		print("Successfully Updated ZipCode:")
		#driver.refresh()	
	except:
		print("Couldnt Load Page refreshing...")
		driver.refresh()
		lowesupdateZip(driver)
def lowesItems(file,link):
	ua = UserAgent()
	header = {'User-Agent':str(ua.random)}
	soruce = requests.get(link,headers = header).text
	soup = BeautifulSoup(soruce, 'lxml')
	grid = soup.find(attrs={"class": "product-cards-grid"})
	value = 1
	item = grid.find(attrs={"data-row":"1"})
	driver = webdriver.Chrome()
	driver.get(link)
	lowesupdateZip(driver)
	while item != None:
		internalLinks = item.find('a')
		links = (internalLinks.get('href'))
		driver.get('https://www.lowes.com' + links)
		totals = "\n\tName Of Product: " + lowesName(driver,links) + "\n\n\t\t" + "Price: " + lowesPrice(driver,links) + "\n\t\t" + "Status: " + lowesgetStock(driver) + "\n\t\t" + "Item Link: " + 'https://www.lowes.com' + links +"\n"
		#print(totals)
		file.write(totals)
		value = value + 1
		item = grid.find(attrs={"data-row":str(value)})
	driver.quit()


def homedepot(toEmail):
	f=open("homeDepotStores.txt", "r")
	homeDepotStores = f.readlines()
	homeDepotFile = open("homeDepot.txt","w+")
	homeDepotFile.truncate(0)
	homeDepotFile.write('-------Home Depot BrigeWater-------\n\n')
	headers = ['\n-------Deep Freezers-------\n']
	index = 0

	for links in homeDepotStores:
		print( "Searching: " + headers[index])
		homeDepotFile.write(headers[index])
		try:
			homeDepotItems(homeDepotFile,links)
		except:
			homeDepotFile.close()
		print( "Completed: " + headers[index])
		index = index + 1
	homeDepotFile.close()
	print("Sending EmailMessage")
	#sendMail("Store Items...", toEmail,"homeDepot.txt")
def lowes(toEmail):
	f=open("lowesStores.txt", "r")
	lowesStores = f.readlines()
	lowesFile = open("lowes.txt","w+")
	lowesFile.truncate(0)
	lowesFile.write('-------Lowes Piscataway-------\n\n')
	headers = ['\n-------Deep Freezers-------\n']
	index = 0

	for links in lowesStores:
		print( "Searching: " + headers[index])
		lowesFile.write(headers[index])
		try:
			lowesItems(lowesFile,links)
		except:
			lowesFile.close()
		print( "Completed: " + headers[index])
		index = index + 1
	lowesFile.close()
	print("Sending EmailMessage")
	#sendMail("Store Items...", toEmail,"lowes.txt")
def walMart():
	f=open("walmartStores.txt", "r")
	walmartStores = f.readlines()
	walmartFile = open("walmart.txt","w+")
	walmartFile.truncate(0)
	walmartFile.write('-------WALMART STUFF-------\n\n')
	headers = ['\n-------Disinfectant Sprays-------\n','\n-------Disinfectant Wipes-------\n']
	index = 0

	for links in walmartStores:
		#print( "Searching: " + headers[index])
		walmartFile.write(headers[index])
		try:
			#print("going inside")
			walmartItems(walmartFile,links)
		except:
			walmartFile.close()
		print( "Completed: " + headers[index])
		index = index + 1
	walmartFile.close()
	print("Sending EmailMessage")
	sendMail("Store Items...", 'cgrant118@gmail.com',"walmart.txt")
	sendMail("Store Items...", 'shugeyalt@gmail.com',"walmart.txt")
def deepFreezers(toEmail):
	#lowes(toEmail)
	homedepot(toEmail)
	sendMail2("Deep Freezers...",toEmail,"lowes.txt","homeDepot.txt")
# link = 'https://www.homedepot.com/b/Appliances-Freezers-Ice-Makers-Chest-Freezers/5-6/N-5yc1vZc3nrZ2bctj7/Ntk-EnrichedProductInfo/Ntt-deep%2Bfreezer?NCNI-5&experienceName=newappliancev3&Ntx=mode%2Bmatchall&lowerBound=0&upperBound=500'
# homeDepotItems('homeDepotStores',link)
walMart()
#homedepot('shugeyalt@gmail.com')
#deepFreezers('shugeyalt@gmail.com')
