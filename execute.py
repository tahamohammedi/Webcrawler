from bs4 import BeautifulSoup
from soup2dict import convert
from deepdiff import DeepDiff
import selenium.webdriver as webdriver
from selenium.webdriver import Chrome
from selenium.webdriver import Firefox
import json
import time
from selenium.webdriver.common.by import By
from utils import *
from webcrawler import *
from pprint import pprint
from selenium.webdriver.firefox.options import Options


# importing command line arguments
args = Args()

options = Options()
options.headless = True
driver = Firefox(options=options, executable_path="/home/taha/Downloads/geckodriver")
driver.get(args.url)
element = driver.find_element(By.TAG_NAME, "body")
page = BeautifulSoup(element.get_attribute('innerHTML'), features="lxml")
# ele.screenshot("./ele.png")
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
	changes = DeepDiff(page_dic, new_page_dic, verbose_level=2, view="tree")
	if changes != {}:
		page = new_page
	pprint(changes)


if __name__ == '__main__':
	main()