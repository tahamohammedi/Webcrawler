import mechanicalsoup
from bs4 import BeautifulSoup
from soup2dict import convert
import json
import time


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
	dic = convert(page)
	print(dic)
if __name__ == '__main__':
	main()