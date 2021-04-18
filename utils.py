def save_cookies(browser):
    return browser.session.cookies.get_dict()


def load_cookies(browser, cookies):
    from requests.utils import cookiejar_from_dict
    browser.session.cookies = cookiejar_from_dict(cookies)

def get_selector(path, data=None):
    path = path.split("root")[1].split("[")
    path.remove('') 
    for i in range(0, len(path)):
        path[i] = path[i].split(']')[0].replace("'", '')
    selector = ''
    if data == "list":
        return path
    for i in range(0, len(path)-1, 2):
        if int(path[i+1]) != 0:
                selector = selector + f'{path[i]}:nth-of-type({int(path[i+1])+1}) > '
        else:
                selector = selector + f'{path[i]} > '
    return selector[:-3]

def print_changes(changes):
    for key in changes:
        if key == "values_changed":
            for item in changes[key]:
                print(f"a {item['name']} was changed from {item['page']} to {item['new_page']}, {item['selector']}")

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

