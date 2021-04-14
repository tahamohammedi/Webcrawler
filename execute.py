import mechanicalsoup
from bs4 import BeautifulSoup
from soup2dict import convert
from deepdiff import DeepDiff
import json
import time
from pprint import pprint


def main(url, timestamp):
	starttime = time.time()
	with open('htm.html') as html:
		page = html.read()
	while True:
		with open('htm.html') as html:
			new_page = html.read()
		trackchange(BeautifulSoup(page, features="lxml"), BeautifulSoup(new_page, features="lxml"))
		time.sleep(timestamp - ((time.time() - starttime) % timestamp))

def trackchange(page, new_page):
	page_dic = convert(page)
	new_page_dic = convert(new_page)
	with open("html.json", "w") as file:
		file.write(json.dumps(page_dic, indent=2))
	output = DeepDiff(page_dic, new_page_dic)
	pprint(output.get("values_changed"))



def get_all_values(nested_dictionary):
	for key, value in nested_dictionary.items():
		print(key, ":", value)
		if type(value) is dict:
			get_all_values(value)
		else:
			print(key, ":", value)


def tracktag():
	pass

if __name__ == '__main__':
	main("https://www.google.com", 3)