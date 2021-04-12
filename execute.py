import mechanicalsoup

def main(url):
	browser = mechanicalsoup.Browser()
	page = browser.get(url)
	print(page)


if __name__ == '__main__':
	main()