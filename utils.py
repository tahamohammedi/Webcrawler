def save_cookies(browser):
    return browser.session.cookies.get_dict()


def load_cookies(browser, cookies):
    from requests.utils import cookiejar_from_dict
    browser.session.cookies = cookiejar_from_dict(cookies)


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
