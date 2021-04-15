import sys
import argparse
import execute
from requests.exceptions import ConnectionError


parser = argparse.ArgumentParser()
parser.add_argument("--url", "-u", help="provide the URL of the web page to watch", required=True)
parser.add_argument("--timestamp",  "-t", help="specifies the delay between each request (a request every 60 seconds is the default value)", type=int, default=60)
parser.add_argument("--login", "-l", help="lets webwatcher know if credentials are needed to access the provided URL", action="store_true")
args = parser.parse_args()

def main():
	urll = url()
	execute.main(urll, args.timestamp)

def url():
	return args.url

def login():
	return args.login


if __name__ == '__main__':
	main()