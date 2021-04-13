import sys
import argparse
import execute
from requests.exceptions import ConnectionError


parser = argparse.ArgumentParser()
parser.add_argument("--url", "-u", help="provide the url of the web page")
parser.add_argument("--timestamp",  "-t", help="specifies the delay between each request (a request every 60 seconds is the default value)", type=int, default=60)


def main():
	args = parser.parse_args()
	url = args.url
	try:
		execute.main(url, args.timestamp)
	except Exception as exception:
		if "Name or service not known" in str(exception):
			print("ConnectionError: URL Could Not Be Found.")
		if "Temporary failure in name resolution" in str(exception):
			return  print("ConnectionError: There's No Internet Connection")
		return print(exception)








if __name__ == '__main__':
	main()