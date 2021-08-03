#wikipedia_summary
import wikipedia as wiki

'''
Written using wikipedia API. Input a string for query, output a summary, 
url from where the summary came from, and suggestions for alternative searches
'''

class WikipediaSummary:

    def __init__(self, term):
        self.term = term

    def lookup(self):
        #returns summary of search item and limits it to 5 sentences
        return wiki.summary(self.term, sentences = 5)

    def suggestions(self):
        #returns related search topics to initial search topic
        return wiki.search(self.term)

    def pagelookup(self):
        #returns link to page
        return wiki.page(self.term).url


def main():
    responses = ['no', 'nope', 'nada', 'negative']
    search = input('what is your question:')
    word = WikipediaSummary(search)
    print(word.lookup())
    print(word.pagelookup())
    keep_going = input('\nWas this what you were looking for?')
    if keep_going.lower() in responses:
        summarylist = str(word.suggestions()).replace('[', '').replace(']','')
        print(f'Hol\' up what about one of these? \n {summarylist}')
        alt_search = input('How about one of these?')
        if alt_search.lower() not in responses:
            newsearch = WikipediaSummary(alt_search)
            newsearch.lookup()
            print(newsearch.lookup())
            print(newsearch.pagelookup())
        else:
            print('\nOh well, I tried.')
    else:
        print('\n')



if __name__ == '__main__':
    main()

