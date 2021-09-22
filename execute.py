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
				Input.send_keys("rafiktoumi96@gmail.com", Keys.ARROW_DOWN)
			if i == 1:
				time.sleep(3)
				Input.send_keys("RafikVisa96!", Keys.ARROW_DOWN)				
		if Input.get_attribute("type") == "submit":
			time.sleep(3)
			Input.submit()
			is_logged = True
			print("Logged in.")
			time.sleep(30)
		i+=1
		"""
from selenium.common.exceptions import TimeoutException

input("Fill in your log in information and submit when the page is fully loaded press Enter:")

loaded = False
while not loaded:
	try:
		WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'li.inactive-link:nth-child(1) > a:nth-child(1)')))
		loaded = True
		driver.find_element_by_css_selector('li.inactive-link:nth-child(1) > a:nth-child(1)').click()
	except TimeoutException: 
		loaded = False

time.sleep(5)


# #dvEarliestDateLnk > div
# initlizing the main itirator for checks
def main():
	starttime = time.time()
	while True:
		original = driver.find_element_by_tag_name("#dvEarliestDateLnk > div")
		#original.screenshot(".original.png")
		driver.refresh()
		new_element = driver.find_element(By.TAG_NAME, "#dvEarliestDateLnk > div")
		new_page = BeautifulSoup(new_element.get_attribute('innerHTML'), features="lxml")
		trackchange(new_page)
		time.sleep(args.timestamp - ((time.time() - starttime) % args.timestamp))
	driver.quit()



# getting changes and printing them
def trackchange(new_page):
	global page
	page_dic = convert(page)
	new_page_dic = convert(new_page)
	changes = get_change(page_dic, new_page_dic)
	if changes["content"] == True:
		page = new_page
		changes = print_changes(changes)
		notification.notify(
				title="There might be available Rendezvous",
				message=changes,
				timeout=100000
			)
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
	ele = driver.find_element_by_css_selector("body")
	image = get_path()
	ele.screenshot(image)
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
