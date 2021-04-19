from bs4 import BeautifulSoup
from soup2dict import convert
from deepdiff import DeepDiff
import selenium.webdriver as webdriver
from selenium.webdriver import Chrome
from selenium.webdriver import Firefox
import json
import glob
import itertools
import os
import time
from selenium.webdriver.common.by import By
from utils import *
from webcrawler import *
from pprint import pprint
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options


# importing command line arguments
args = Args()

options = Options()
options.headless = True
driver = Firefox(options=options, executable_path="/webdrivers/geckodriver")
driver.get(args.url)
element = driver.find_element(By.TAG_NAME, "body")
page = BeautifulSoup(element.get_attribute('innerHTML'), features="lxml")
#ele.screenshot("./ele.png")
def main():
	starttime = time.time()
	while True:
		driver.refresh()
		new_element = driver.find_element(By.TAG_NAME, "body")
		new_page = BeautifulSoup(new_element.get_attribute('innerHTML'), features="lxml")
		trackchange(new_page)
		time.sleep(args.timestamp - ((time.time() - starttime) % args.timestamp))
	driver.quit()


def trackchange(new_page):
	global page
	page_dic = convert(page)
	new_page_dic = convert(new_page)
	changes = get_change(page_dic, new_page_dic)
	if changes["content"] == True:
		page = new_page
		print_changes(changes)
	print({})


def get_screenshot(changes):
	global driver
	for item in changes:
		script = f"""
		var element = document.querySelector('{item['selector']}');
		element.style.background='red';
		var rect = element.getBoundingClientRect();
		return rect
		"""
		rect = driver.execute_script(script)
	ele = driver.find_element_by_css_selector("body")
	image = get_link()
	ele.screenshot(image)
	get_map(image, rect)
	return


def get_link():
	list_of_files = glob.glob('screenshots/*')
	if list_of_files != []:
		latest_file = max(list_of_files, key=os.path.getctime)
		file = latest_file[:-4]
		number = file[-1]
		file = f"screenshots/ele{int(number)+1}.png"
	else: file = "screenshots/ele0.png"
	return file


def get_map(image, rect):
	with open(f"image.html", "w") as file:
		file.write(f"""
			<img src="{image}" alt="Workplace" usemap="#workmap">
			<map name="workmap">
			<area shape="rect" coords='{rect}' onclick="clicked()">
			<script>
			function clicked() {{
				alert("{image}")
			}}
			</script>
			""")
if __name__ == '__main__':
	main()