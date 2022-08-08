# Webcrawler (Beta Version)
A tool to monitor websites and detect changes with visual presentation.

# Setting up
  To set up Webcrawler you should clone this git repository and install the requirements:  
Note: you should at least have Python 3.8 (a virtual environment is recommended) and Firefox installed.

```
git clone https://github.com/tahamohammedi/Webcrawler
cd Webcrawler
pip install -r requirements.txt
```

# Usage 

Webcrawler takes three arguments (url, time, headless, element), you pass the url of the web page you intend to monitor and how frequently it should be checked.

Example:
```
python webcrawler.py --url="https://www.unixtimestamp.com/" --time=10
```
This will make Webcrawler check the page "https://www.unixtimestamp.com/" every 10 seconds.

and the following should be printed:
```
a div was changed
a span was changed
a td was changed
a td was changed
a td was changed
a td was changed
Checks: 1
```
  To see what changed visually, go to ```/screenshots```, every website you pass to ```url``` will make directories and subdirectories depending on the website's name and how many routes are in the url (in our case it's just ```/screenshots/www.unixtimestamp.com```), In every check two images get saved in their respective directory ```orignal.png``` and ```compared.png``` (supposing it's the first check: ```original0.png``` and ```compared0.png``` will be stored and the numbers will increase in every check), ```original.png``` is the original state of the page before the change and ```compared.png``` is the state after the change with every element that changed bordered in green

```oringal0.png``` should look something like this:
![alt text](/doc/original1.png "original.png")
```changed0.png``` should look something like this:
![alt text](/doc/compared1.png "compared1.png")


## Aditional features:
Passing ```-h``` or ```--headless``` will hide the browser attached to Webcrawler.

If you want to watch one HTML element specifically you can pass the CSS selector to ```--element``` or ```-e```

Example: 
```
python webcrawler.py --url="https://www.unixtimestamp.com/" --time=10 --headless --element="#main-segment > div.box > div > div.ui.two.column.grid > div > div:nth-child(2) > div > div.value.epoch"
```

