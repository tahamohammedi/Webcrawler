import sys
import argparse
import execute
from requests.exceptions import ConnectionError


parser = argparse.ArgumentParser()
parser.add_argument("--url", "-u", help="provide the url of the web page")



def main():
	args = parser.parse_args()
	url = args.url
	execute.main(url)











if __name__ == '__main__':
	main()