#https://crinacle.com/rankings/iems/
#https://crinacle.com/rankings/headphones/
import requests
import pandas as pd

'''
Audiophile.py is used as a web scraper for looking through crinacle.com's ranking sectins for iems and headphones.
This will pull the table, and then based on user paramters of price and sound type it will output products that
follow those parameters.
'''

class AudiophileGear:
    def __init__(self, gear, price, top):
        self.gear = gear #are you looking for iems or headphones?
        self.price = price #what is the price max?
        self.top = top #for search results? do you want top 5? top 10? all of them?
        if self.gear.lower() == 'iems':
            self.url = 'https://crinacle.com/rankings/iems/'
        if self.gear.lower() == 'headphones':
            self.url = 'https://crinacle.com/rankings/headphones/'
        self.premature = None #will hold initial pull from website, and will hold modifications
        self.results = None #will hold the soon to be outputed results
    def gear_search(self):
        '''Use pandas library to pull table from website '''
        #nifty pandas function that will find a table on a website and store it as text
        #it is initially stored in a list, that is why there is a [0] at the end of the return
        self.premature = pd.read_html(requests.get(self.url).text)[0]

    def morph_search(self):
        '''Morph pandas df to users desired output'''
        #grab 4 columns that matter from the website's table
        self.premature = self.premature[['Rank','Model','Price (MSRP)','Comments']]
        #Drop all C-F tier audio equipment
        #
        self.premature = self.premature[~self.premature['Rank'].str.contains('C')]
        self.premature = self.premature[~self.premature['Rank'].str.contains('D')]
        self.premature = self.premature[~self.premature['Rank'].str.contains('E')]
        self.premature = self.premature[~self.premature['Rank'].str.contains('F')]
        #
        #remove any letters or question marks in the price section and replace with 0
        self.premature['Price (MSRP)'] = self.premature['Price (MSRP)'].replace(regex='([?a-zA-Z])', value = 0)
        #convert all the values in price from strings to numbers. useful for price checking later on.
        self.premature['Price (MSRP)'] = pd.to_numeric(self.premature['Price (MSRP)'])
    
    def filter_search(self):
        '''Based on user restrictions shoot out the appropriate output'''
        self.results = self.premature
        if self.price != None:
            #if the price is set use it and make self.results that
            self.results = self.results.loc[self.results['Price (MSRP)'] <= self.price]
            self.results = self.results[self.results['Price (MSRP)'] != 0]
        if self.top != None:
            #if the number of results are specified show that
            self.results = self.results.head(self.top)
        return self.results

def main():
    start = AudiophileGear('iems', 200, None)
    start.gear_search()
    start.morph_search()
    print(start.filter_search())

if __name__ == '__main__':
    main()
