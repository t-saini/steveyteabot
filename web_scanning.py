import requests
import datetime
from bs4 import BeautifulSoup
import utility
import wikipedia as wiki

def find_posh(setup = utility.run_ini()):
    url = setup['web']['url1']
    header = {'User-Agent':setup['web']['user']}
    requesturl = requests.get(url, headers = header)
    soup = BeautifulSoup(requesturl.text, 'html.parser')
    results_main = soup.find('div', {'tiles_container m--t--1'})
    crude_links = [a['href'] for a in results_main.find_all('a', href=True) if a.text]
    links_to_ship = []
    for link in crude_links:
        if '/listing' in link:
            links_to_ship.append('https://poshmark.com'+link)
    return links_to_ship

def dapper_up(setup = utility.run_ini()):
    url = setup['web']['url2']
    header = {'User-Agent':setup['web']['user']}
    requesturl = requests.get(url, headers = header)
    soup = BeautifulSoup(requesturl.text, 'html.parser')
    results_main = soup.find('div', {'class':'home-top widget-area'})
    article = results_main.find('div', {'class':'widget-wrap'})
    links = []
    post = []
    times = article.find_all('time')
    for time in times:
        today = datetime.date.today().strftime("%Y-%m-%d")
        formated_time = str(time).split(' ')[2].split('T')[0][10:]
        if str(today) == str(formated_time):
            post.append(formated_time)
    link_anchors = article.find_all(href=True)
    for link_anchor in link_anchors:
        if 'aria-hidden' in str(link_anchor):
            # crude_link = str(link_anchor).split(' ')[3].split('>')[0]
            continue
        crude_link = str(link_anchor).split(' ')[1].split('>')[0]
        link_start = crude_link.find('\"') + 1
        link_end = crude_link[link_start:].find('\"')
        link = crude_link[link_start:link_start+link_end]
        links.append(link)
    return links[0:len(post)]

def wiki_search(term):
    domain = 'https://en.wikipedia.org/wiki/'
    suggestions = wiki.search(term)
    page = domain + term.replace(' ','_')
    return suggestions, page

if __name__ == "__main__":
    #print(find_posh())
    print(dapper_up())