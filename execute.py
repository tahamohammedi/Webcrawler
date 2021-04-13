import mechanicalsoup
import json
import time

def main(url, timestamp):
	starttime = time.time()
	with open('htm.html') as html:
		page = html.read()
	while True:
		with open('htm.html') as html:
			new_page = html.read()
		trackchange(page, new_page)
		time.sleep(timestamp - ((time.time() - starttime) % timestamp))

def trackchange(page, new_page):
	with open('htm.json') as js:
		page_json = json.loads(js.read())

	print(page_json["body"])

if __name__ == '__main__':
	main()