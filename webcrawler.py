import mechanicalsoup
import requests
import sys
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--url", "-u", help="provide the url of the web page")


def main():
	args = parser.parse_args()
	url = args.url
	try:
		response = requests.get(url)
	except requests.ConnectionError as exception:
		if "Temporary failure in name resolution" in str(exception):
			raise  Exception("ConnectionError: There's No Internet Connection")
		elif "Name or service not known" in str(exception):
			raise Exception("ConnectionError: URL Could Not Be Found.")

	browser = mechanicalsoup.Browser()
	page = browser.get(url)
	print(page)









if __name__ == '__main__':
	main()