import web_scanning
import slickdeals as slick
import utility

welcome_messages = {0: 'H U L L O', 
1: 'Hullo, anyone want tea?🐱‍👓', 
2:'Yo I\'m trying to sleep', 
3:'Where my brown bear at?'}

tangisms = {0:'expensive hot tea leaf juice...add black balls and asians will love you', 
1: 'Yo I\'m trying to sleep', 
2: 'you do be lookin kinda cute today',
3: 'posture check mofucka', 
4: 'I only speak to himbos', 
5:'Sleepy Joe? I am all about Dark Brandon', 
6:'I have seen a cautionary reddit tale come to life...anything is possible.', 
7:'We have all bore witness to a man get that phat fiscal SUCC',
8:'H U L L O', 
9: 'Hullo, anyone want tea?🐱‍👓', 
10:'Yo I\'m trying to sleep', 
11:'Where my brown bear at?', 
12:'Bro I\'m Chinese what do you want from me...'}

quips = {0:'Found some fresh fits at a fair price',
        1:'Who said lookin\' good has to be pricey', 
        2:'Comin\' in hot with some new threads', 
        3: 'Best dressed incoming', 
        4:'I like my money right where I can see it: hanging in my closet.',
        5:'If you can’t be better than your competition, just dress better.',
        6:'Buy less, choose well.' }


def summon_message():
    return utility.gen_random_int(welcome_messages)

def birthday_message():
    return 'HAPPY BIRTHDAY 🎈🎉🐱‍👓'

def help_message():
    return '''
    I\'m a simple bot modeled after the great Sleeping Dragon Steven Tang.\n
    !wiki [topic] - ex: !wiki Godzilla | !wiki Nine Inch Nails \n
    !deals [item] - ex: !deals speakers | !deals Tool Vinyl \n
    !audio [styel of headphones] [prince max] - ex: !audio iems 200 \n
    I also monitor the following: dappered.com and poshmart.com for new sales. 🐱‍👓
    '''

def quip_message():
    selected = utility.gen_random_int(tangisms)
    return tangisms[selected]

def wiki_message(message):
    search = message.content.lower().replace('!wiki ', '')
    suggestion, link = web_scanning.wiki_search(search)
    phrase = f'here\'s the sauce degens: {link} \n'\
    'if this isn\'t what you wanted, i tried 🤷‍♂️ so, try one of those below.'
    summarylist = str(suggestion).replace(
            '[', '').replace(']', '')
    result = f'{phrase} \n {summarylist}'
    return result


def deals_message(message):
    item = message.content.lower().replace('!deals ', '')
    outputls=[]
    deal_search = slick.SlickSearch(message.content)
    deal_search.crawl_search()
    deal_search.gen_deals()
    output = deal_search.display_deals()
    if len(output) == 0:
        return f'sorry my guy, i couldn\'t find any deals for {item} 😕'
    outputls.append(f'Did someone say they needed a deal on {item}, '\
        f'Full Results: {deal_search.full_url()}? \n')
    for row in output.index:
        selected_row = list(output.iloc[row])
        msg = f'{selected_row[0]} Priced at: {selected_row[1]}\n '\
            f'{selected_row[2]} \n'
        outputls.append(msg)
    return ' '.join(outputls)


def audio_message(message:str):
    inputls = message.content.lower().split(' ')[1:]
    outputls = []
    try:
        gear = inputls[0]
        price = int(inputls[1])
        recommendation_df = web_scanning.find_audiogear(price, gear)
        if len(recommendation_df) == 0:
            return 'I found nothing at that price point 😛🐱‍💻'
        for row in recommendation_df.index:
            selected_row = list(recommendation_df.iloc[row])
            msg = (f"Priced at ${selected_row[2]}, {selected_row[1]} has a {selected_row[3]} "
                f"sound signature with {selected_row[4]}. I\'d give this a {selected_row[0]}\n")
            outputls.append(msg)
        return ' '.join(outputls)
    except (TypeError, ValueError):
        return f'Uh oh I ran into an error, try doing the gear first and then the price 🐱‍💻'
        
