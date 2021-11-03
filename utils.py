from deepdiff import DeepDiff
from pprint import pprint
import execute


def save_cookies(browser):
    return browser.session.cookies.get_dict()


def load_cookies(browser, cookies):
    from requests.utils import cookiejar_from_dict
    browser.session.cookies = cookiejar_from_dict(cookies)


# getting css selector from deepdiff.path()
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


# printing changes and calling get_screenshot()
def print_changes(changes):
    for key in changes:
        if changes.get(key):
            if key.split('_')[-1] != "removed":
                execute.get_screenshot(changes[key])
            for item in changes[key]:
                print(f"a {item['name']} was {key.split('_')[-1]}")



# storing changes for later use
def get_change(page, new_page):
    changes = {
        "values_changed": [],
        "dictionary_item_added": [],
        "dictionary_item_removed": [],
        "iterable_item_added": [],
        "iterable_item_removed": [],
    }
    changes_dic = dict(DeepDiff(page, new_page, verbose_level=2, view="tree", ignore_string_type_changes=True, ignore_numeric_type_changes=True, exclude_regex_paths=["attrs", "script"]))
    if changes_dic:
        for key in changes_dic:
            if changes_dic.get(key) and key in changes.keys():
                for change in changes_dic[key]:
                    changes[key].append({
                    "page": change.t1,
                    "new_page": change.t2,
                    "selector": get_selector(change.path()),
                    "name": get_name(change, key.split('_')[-1])
                        })

    return changes

def get_name(change, change_type):
    global name
    try:
        if change_type != "removed":
            if type(change.t2) == list: 
                name = change.t2[0]["name"]
            else:
                name = change.t2["name"]
        else:
            if type(change.t1) == list: 
                name = change.t1[0]["name"]
            else:
                name = change.t1["name"]
    except TypeError:
        return get_name(change.up, change_type)
    finally:
        return name
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

