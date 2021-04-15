import mechanicalsoup
from bs4 import BeautifulSoup
from soup2dict import convert
from deepdiff import DeepDiff
import json
import time
from webcrawler import *
from pprint import pprint

def save_cookies(browser):
    return browser.session.cookies.get_dict()

def load_cookies(browser, cookies):
    from requests.utils import cookiejar_from_dict
    browser.session.cookies = cookiejar_from_dict(cookies)

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


browser = mechanicalsoup.StatefulBrowser()
page = browser.get(url())
page

if login() == True:
	i = 0
	form_not_found = True
	while form_not_found:
		form_selector = input("provide form css selector: ")
		print(page.soup)
		exit()
		with open("html.json", "w") as file:
			file.write(json.dumps(convert(page), indent=2))
		if page.select(form_selector) == []:
			print(bcolors.FAIL + "No form found with provided selector." + bcolors.ENDC)
		else:
			form = page.select(form_selector)
			form_not_found = False
	form = page.select(form_selector)
	form = form[0]
	for inputs in form.select("input"):
		if inputs["type"] != "hidden" and inputs["type"] != "submit" and inputs["type"] != "button":
			value = input(f"fill up the input ({inputs['name']}): ")
			form.select("input")[i]["value"] = value
		i += 1
	profile = browser.submit(form, url())
	cookies = save_cookies(browser)
	page = browser.get(url())
	page = page.soup

def main(url, timestamp):
	starttime = time.time()
	while True:
		load_cookies(browser, cookies)
		new_page = browser.get(url)
		trackchange(new_page.soup, url)
		time.sleep(timestamp - ((time.time() - starttime) % timestamp))

def trackchange(new_page, url):
	global page
	selector = """#repo-content-pjax-container > div > div.gutter-condensed.gutter-lg.flex-column.flex-md-row.d-flex > div.flex-shrink-0.col-12.col-md-9.mb-4.mb-md-0 > div.Box.mb-3 > div.js-details-container.Details > div.Details-content--hidden-not-important.js-navigation-container.js-active-navigation-container.d-md-block"""

	page_dic = convert(page.select(selector))
	new_page_dic = convert(new_page.select(selector))
	with open("htm.json", "w") as file:
			file.write(json.dumps(page_dic, indent=2))
	changes = DeepDiff(page_dic, new_page_dic, exclude_regex_paths="input")
	if changes != {}:
		with open("html.json", "w") as file:
			file.write(changes.to_json(indent=2))
		page = new_page
	pprint(changes)



if __name__ == '__main__':
	main()