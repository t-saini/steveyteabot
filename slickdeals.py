#slickdeals
import requests
from bs4 import BeautifulSoup
import pandas as pd


class SlickSearch:
    '''
    Modified and adapted from https://github.com/MinweiShen/slickdeals
    Moved away from command line based interactions for ease of adpation into Discord Bot
    Discord Bot used on message events intso of commands. This was done for simplicity reasons.

    Discord python Bot passes in users message of what they are looking for, output are the top 5
    deals regardless if they are expired along with the link to the full search page. Pandas was used for
    visual aesthetic reasons for preenting data
    '''
    def __init__(self, search):
        #swaps !deals from search term with nothing
        self.search = search.replace('!deals','')
        #first segment of url
        self.slickdeals = 'https://slickdeals.net/'
        #second segment of url before search term
        self.searchurl1 = 'newsearch.php?q='
        #fourth segment of url after search term
        self.seaerchurl2 ='&searcharea=deals&searchin=first'
        #thesea re the raw results from the url page
        self.results = None
        #dictionary that will neatly store product information in a dictionary
        self.deals = {'Product': [], 'Price': [],'Link': [],  'Info': []}
        #full url that is in the browser
        self.url = None

    def crawl_search(self):
        '''Goes to url and scrapes results from div'''
        self.url = str(self.slickdeals+self.searchurl1+self.search+self.seaerchurl2).replace(' ', '%20')
        requesturl = requests.get(self.url)
        #parse through the html
        soup = BeautifulSoup(requesturl.text,'html.parser')
        #find the div with data-modulename Search results
        self.results = soup.find('div', {'data-module-name': 'Search Results'})
        #pull the results
        self.results = self.results.find_all('div', {'class': 'resultRow'})

    def gen_deals(self):
        for results in self.results:
            anchor = results.find('a', {'class': 'dealTitle'})
            self.deals['Product'].append(anchor['title'])
            self.deals['Link'].append(self.slickdeals[0:-1]+anchor['href'])
            self.deals['Price'].append(results.find('span',{'class':'price'}).getText().strip())
            rating = results.find('div', {'class': 'ratingNum'}).getText().strip()
            expired = 'Expired' if 'expired' in results['class'] else ''
            self.deals['Info'].append(f'{rating} {expired}')

    def display_deals(self):
        dataframe = pd.DataFrame.from_dict(self.deals, orient='columns')
        #top 5 deals should be enough
        #discord limits tabulation in messages, to_markdown attempts to make these messages nicer looking
        top_five = dataframe[['Product','Price','Link']].head(5)
        return top_five

    def full_url(self):
        return self.url


def main():
    start = SlickSearch('Sony Bluetooth Headphones')
    start.crawl_search()
    start.gen_deals()
    print(start.display_deals())

if __name__ == '__main__':
    main()
