from bs4 import BeautifulSoup
from soup2dict import convert
from deepdiff import DeepDiff
import selenium.webdriver as webdriver
from selenium.webdriver import Chrome
from selenium.webdriver import Firefox
from shutil import copyfile
import json
import glob
import itertools
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
options.headless = True
driver = Firefox(options=options, executable_path="webdrivers/geckodriver")

watch = input("Provide the css selector of the element to watch:")
#watch="body"

driver.get(args.url)

element = driver.find_element(By.TAG_NAME, watch)
page = BeautifulSoup(element.get_attribute('innerHTML'), features="lxml")

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
 # watch: 
	for Input in inputs:
		if Input.get_attribute("type") != "hidden" and Input.get_attribute("type") != "submit" and Input.get_attribute("type") != "button":
			value = input(f"fill up the input ({Input.get_attribute('name')}): ")
			time.sleep(3)
			Input.send_keys(value, Keys.ARROW_DOWN) 
		if Input.get_attribute("type") == "submit":
			Input.submit()





# initlizing the main itirator for checks
def main():
	starttime = time.time()
	while True:
		original = driver.find_element_by_css_selector(watch)
		original.screenshot(".original.png")
		driver.refresh()
		new_element = driver.find_element(By.CSS_SELECTOR, watch)
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
	if changes.values():
		page = new_page
		print_changes(changes)
	print({})





# sylize changed parts and get a screenshot
def get_screenshot(changes):
	global driver, watch

	for item in changes:
		style_item(item['selector'], "green")

	ele = driver.find_element_by_css_selector(watch)
	image = get_path()
	ele.screenshot(image)

	for item in changes:
		unstylize_item(item['selector'])

	get_original()
	return






def style_item(selector, color):
	selector = selector[11:]
	selector = watch + selector
	script = f"""
		var element = document.querySelector('{selector}');
		element.style.border='2px solid {color}';
		"""
	driver.execute_script(script)

def unstylize_item(selector):
	script = f"""
		var element = document.querySelector('{selector}');
		element.style.border='none';
	"""
	driver.execute_script(script)


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
