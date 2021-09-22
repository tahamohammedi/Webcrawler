import sys
import argparse
import execute
from utils import *
import traceback
import time
from requests.exceptions import ConnectionError
from plyer import notification


parser = argparse.ArgumentParser()
parser.add_argument("--url", "-u", help="provide the URL of the web page to watch", required=True)
parser.add_argument("--timestamp",  "-t", help="specifies the delay between each check in seconds (a check every 60 seconds is the default value)", type=int, default=60)
parser.add_argument("--login", "-l", help="lets webcrawler know if credentials are needed to access the page of the provided URL", action="store_true")
parser.add_argument("--element", "-e", help="specify the specific element you want to track")
args = parser.parse_args()


def main():
	try:
		execute.main()
	except:
		notification.notify(
				title="Webcrawler: There was an error",
				message="check it out bruh",
				timeout=100000
			)		
		traceback.print_exc()

class Args:
    url = args.url
    login = args.login
    timestamp = args.timestamp
    element = args.element


if __name__ == '__main__':
	main()