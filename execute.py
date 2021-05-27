import mechanicalsoup
from bs4 import BeautifulSoup
from soup2dict import convert
from pushbullet import PushBullet
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

def push_message(title, body):
	pb = PushBullet("o.MiKj6c4KFhgjbWQ53MAyOA1t0WDaHWmx")
	pb.push_note(title, body)

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
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.75 Safari/537.36',
'Origin': 'candidature.1337.ma',
'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
'Referer': f'{url()}'}
page = browser.get(url(), headers=headers)
page = page.soup
selector = "body"

if login() == True:
	i = 0
	form_not_found = True
	while form_not_found:
		print(page)
		form_selector = input("provide form css selector: ")
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
	print("Logged in.")
	selector = input("provide element selector: ")
	page = page.soup

def main(url, timestamp):
	starttime = time.time()
	while True:
		load_cookies(browser, cookies)
		new_page = browser.get(url)
		trackchange(new_page.soup, url)
		time.sleep(timestamp - ((time.time() - starttime) % timestamp))

def trackchange(new_page, url):
	global page, selector
	page_dic = convert(page.select(selector))
	new_page_dic = convert(new_page.select(selector))
	changes = DeepDiff(page_dic, new_page_dic)
	if changes != {}:
		push_message("changes occured", "42 might have spots")
		page = new_page
		with open("page.html", "w") as jsfile:
			jsfile.write(json.dumps(changes, indent=2))
	pprint(changes)



if __name__ == '__main__':
	main()