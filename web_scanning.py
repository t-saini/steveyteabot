import requests
import datetime
from bs4 import BeautifulSoup
from bs4 import SoupStrainer
import utility
import wikipedia as wiki
import pandas as pd


def find_posh(setup = utility.run_ini()):
    links_to_ship = {0:[],1:[],2:[],3:[]}
    urls = [setup['web']['url1'], setup['web']['url3'], 
        setup['web']['url4'], setup['web']['url5']]
    for index, url in enumerate(urls):
        header = {'User-Agent':setup['web']['user']}
        requesturl = requests.get(url, headers = header)
        soup = BeautifulSoup(requesturl.text, 'html.parser')
        results_main = soup.find('div', {'tiles_container m--t--1'})
        crude_links = [a['href'] for a in results_main.find_all('a', href=True) if a.text]
        for link in crude_links:
            if '/listing' in link:
                links_to_ship[index].append('https://poshmark.com'+link)
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

def find_audiogear(price:int,gear_type:str):
    setup = utility.run_ini()
    url = setup['web']['url6']+gear_type
    tab = setup['misc'][gear_type]
    requesturl = requests.get(url, headers = {'User-Agent':setup['web']['user']})
    strainer = SoupStrainer('table', {'id': tab})
    soup = BeautifulSoup(requesturl.text, 
        'html.parser', parse_only=strainer)
    results_pd = pd.read_html(str(soup))[0]
    results = results_pd[['Rank', 'Model', 'Price (MSRP)', 
        'Signature', 'Comments']].copy()
    results = results[results['Rank'].str.contains('|'.join(['S','A','B']))]
    str_remove = list(results['Price (MSRP)'].str.extract(r'^([aA-zZ ]*)')[0].unique())
    remove_these = [s for s in str_remove if s.strip() !='']
    remove_iems = 'qdc 8SL/Gemini/Anole VX'
    results = results[(results['Model']!=remove_iems) & (results['Price (MSRP)']!='?')]
    results = results[~results['Price (MSRP)'].str.contains('|'.join(remove_these))]
    results['Price'] = results['Price (MSRP)'].str.extract(r'^([0-9]*)').astype(int)
    results = results[['Rank', 'Model', 'Price', 
        'Signature', 'Comments']]
    sorted_results = results[results['Price']<=price].sort_values(
        by=['Price','Signature'], ascending=False).head(5)
    return sorted_results.reset_index(drop = True)


if __name__ == "__main__":
    # find_posh()
    # dapper_up()
    find_audiogear(100,'headphones')