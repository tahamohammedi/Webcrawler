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
#options.headless = True
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
	changes = get_change(page_dic, new_page_dic)
	if changes["content"] == True:
		page = new_page
		print_changes(changes)
	print({})

def get_change(page, new_page):
	changes = {
		"values_changed": [],
		"dictionary_item_added": [],
		"dictionary_item_removed": [],
		"iterable_item_added": [],
		"iterable_item_removed": [],
		"content": False
	}
	changes_dic = dict(DeepDiff(page, new_page, verbose_level=2, view="tree", ignore_string_type_changes=True, ignore_numeric_type_changes=True, exclude_regex_paths=["attrs", "script"]))
	if changes_dic.get("values_changed"):
		changes["content"] = True
		for change in changes_dic.get("values_changed"):
			changes["values_changed"].append({
				"page": change.t1,
				"new_page": change.t2,
				"selector": get_selector(change.path()),
				"name": change.up.t2["name"]
			})

	return changes

if __name__ == '__main__':
	main()