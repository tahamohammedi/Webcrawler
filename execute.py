from bs4 import BeautifulSoup
from soup2dict import convert
from deepdiff import DeepDiff
import selenium.webdriver as webdriver
from selenium.webdriver import Chrome
import json
import time
from utils import *
from webcrawler import *
from pprint import pprint

# importing command line arguments
args = Args()

options = webdriver.ChromeOptions()
options.binary = "/webdrivers/chromedriver"
print(options.binary)
driver = Chrome(chrome_options=options)
print(driver)


def main():
	"""
	starttime = time.time()
	while True:
		load_cookies(browser, cookies)
		new_page = browser.get(url)
		trackchange(new_page.soup, url)
		time.sleep(timestamp - ((time.time() - starttime) % timestamp))"""


def trackchange(new_page, url):
	global page
	selector = """
	#repo-content-pjax-container > div > div.gutter-condensed.gutter-lg.flex-column.flex-md-row.d-flex >
	div.flex-shrink-0.col-12.col-md-9.mb-4.mb-md-0 > div.Box.mb-3 > div.js-details-container.Details >
	div.Details-content--hidden-not-important.js-navigation-container.js-active-navigation-container.d-md-block"""

	page_dic = convert(page.select(selector))
	new_page_dic = convert(new_page.select(selector))

	changes = DeepDiff(page_dic, new_page_dic, exclude_regex_paths="input")
	if changes != {}:
		page = new_page
	pprint(changes)



if __name__ == '__main__':
	main()