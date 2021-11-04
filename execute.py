from bs4 import BeautifulSoup
from soup2dict import convert
from deepdiff import DeepDiff
import selenium.webdriver as webdriver
from selenium.webdriver import Chrome
from selenium.webdriver import Firefox
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from shutil import copyfile
from selenium.webdriver.support.ui import Select
from plyer import notification
import json
import glob
import itertools
import pickle 
import os
import urllib.parse
import time
from selenium.webdriver.common.by import By
from utils import *
from webcrawler import *
import re
from pprint import pprint
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options




# importing command line arguments
args = Args()





# creating the neccessary directories 
parsed = urllib.parse.urlparse(args.url)
page_name = str(parsed.netloc)+str(parsed.path)
if not os.path.exists(f"screenshots/{page_name}"):
	os.makedirs(f"screenshots/{page_name}")



# intiating the browser and storing the intial page
options = Options()
# options.headless = True
driver = Firefox(options=options, executable_path="webdrivers/geckodriver")
driver.get(args.url)
element = driver.find_element(By.TAG_NAME, "body")
page = BeautifulSoup(element.get_attribute('innerHTML'), features="lxml")


"""
if Args.login == True:
	i = 0
	form_not_found = True

	while form_not_found:
		form_selector = input("provide form css selector: ")
		if page.select(form_selector) == []:
			print(bcolors.FAIL + "No form found with provided selector." + bcolors.ENDC)
		else:
			form = driver.find_element_by_css_selector(form_selector)
			form_not_found = False

	inputs = form.find_elements_by_tag_name("input")

 # li.inactive-link:nth-child(1) > a:nth-child(1)
	is_logged = False
	i=0
	for Input in inputs:
		if Input.get_attribute("type") != "hidden" and Input.get_attribute("type") != "submit" and Input.get_attribute("type") != "button":
			if i == 0:
				time.sleep(3)
				Input.send_keys("", Keys.ARROW_DOWN)
			if i == 1:
				time.sleep(3)
				Input.send_keys("", Keys.ARROW_DOWN)				
		if Input.get_attribute("type") == "submit":
			time.sleep(3)
			Input.submit()
			is_logged = True
			print("Logged in.")
			time.sleep(30)
		i+=1
		"""
from selenium.common.exceptions import TimeoutException

input("Fill in your log in information and submit. \nwhen the page is fully loaded press Enter:")
time.sleep(2)
loaded = False
while not loaded:
	try:
		WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'li.inactive-link:nth-child(1) > a:nth-child(1)')))
		loaded = True
	except TimeoutException: 
		loaded = False
driver.find_element_by_css_selector('li.inactive-link:nth-child(1) > a:nth-child(1)').click()
time.sleep(2)

loaded = False
while not loaded:
	try:
		WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#VisaCategoryId')))
		loaded = True
	except TimeoutException: 
		loaded = False
driver.find_element_by_css_selector('#VisaCategoryId').click()
time.sleep(2)

loaded = False
while not loaded:
	try:
		WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#VisaCategoryId > option:nth-child(10)')))
		loaded = True
		driver.find_element_by_css_selector('#VisaCategoryId > option:nth-child(10)').click()
	except TimeoutException: 
		loaded = False



time.sleep(5)


# #dvEarliestDateLnk > div
# initlizing the main itirator for checks
def main():
	starttime = time.time()
	while True:
		#original = driver.find_element_by_tag_name("#dvEarliestDateLnk > div")
		#original.screenshot(".original.png")
		driver.refresh()
		time.sleep(2)
		driver.switch_to_alert().accept()
		trackchange()
		time.sleep(args.timestamp - ((time.time() - starttime) % args.timestamp))
	driver.quit()


# #btnContinue 
# getting changes and printing them
def trackchange():
	global page
	loaded = False
	while not loaded:
		try:
			WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#dvEarliestDateLnk > div')))
			loaded = True
			driver.find_element_by_css_selector('#dvEarliestDateLnk > div')
			driver.execute_script("document.querySelector('#dvEarliestDateLnk > div').style.display = 'block';")
		except TimeoutException: 
			loaded = False

	slots = driver.find_element_by_css_selector("#dvEarliestDateLnk > div")
	print(slots.text)
	if "Earliest slot available on" in slots.text:
		time.sleep(2)
		loaded = False
		while not loaded:
			try:
				WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#dvEarliestDateLnk > div')))
				loaded = True
				driver.find_element_by_css_selector('#dvEarliestDateLnk > div')
				driver.execute_script("document.querySelector('#dvEarliestDateLnk > div').style.display = 'none';")
			except TimeoutException: 
				loaded = False

		btncontinue = driver.find_element_by_css_selector("#btnContinue").click()


		time.sleep(3)
		loaded = False
		while not loaded:
			try:
				WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div[1]/div[3]/div[2]/a')))
				loaded = True
				driver.find_element_by_xpath('/html/body/div[2]/div[1]/div[3]/div[2]/a').click()
			except TimeoutException: 
				loaded = False

		time.sleep(3)
		driver.find_element_by_css_selector("#PassportNumber").send_keys("4938023")

		time.sleep(2)
		driver.find_element_by_css_selector("#DateOfBirth").send_keys("12/12/1996")
		driver.find_element_by_css_selector("#PassportExpiryDate").send_keys("03/06/2025")

		time.sleep(2)
		select = Select(driver.find_element_by_css_selector('#NationalityId'))

		select.select_by_value('161')
		time.sleep(2)
		driver.find_element_by_css_selector("#submitbuttonId").click()

	print({})


# sylize changed parts and get a screenshot
def get_screenshot(changes):
	global driver
	for item in changes:
		script = f"""
		var element = document.querySelector('{item['selector']}');
		element.style.border='2px solid green';
		"""
		driver.execute_script(script)
	ele = driver.find_element_by_css_selector("#dvEarliestDateLnk > div")
	content = ele.get_attribute("innerHTML")
	script = f"var element = document.querySelector('#dvEarliestDateLnk > div');element.style.display=''"
	driver.execute_script(script)

	image = get_path()
	ele.screenshot(image)

	with open("page.html", "w") as outfile:
		outfile.write(content)

	for item in changes:
		script = f"""
		var element = document.querySelector('{item['selector']}');
		element.style.border='none';
		"""
		driver.execute_script(script)
	get_original()
	return

# getting the path of the next image based on the last one created
def get_path():
	global page_name
	list_of_files = glob.glob(f'screenshots/{page_name}/*')
	if list_of_files != []:
		latest_file = max(list_of_files, key=os.path.getctime)
		file = latest_file[:-4]
		number = file[-1]
		file = f"screenshots/{page_name}/compared{int(number)+1}.png"
	else: file = f"screenshots/{page_name}/compared0.png"
	return file


# getting the image before the change
def get_original():
	global page_name
	list_of_files = glob.glob(f'screenshots/{page_name}/*')
	if list_of_files != []:
		latest_file = max(list_of_files, key=os.path.getctime)
		file = latest_file[:-4]
		number = file[-1]
	else: number = 0
	copyfile(".original.png", f'screenshots/{page_name}/original{int(number)}.png')

if __name__ == '__main__':
	main()
