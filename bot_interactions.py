import web_scanning
import slickdeals as slick
import audiophile
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
    #if bot is not the author try to take the item metioned through slickdeals module
    try:
        deal_search = slick.SlickSearch(message.content)
        deal_search.crawl_search()
        deal_search.gen_deals()
        output = deal_search.display_deals()
        #message out with deal informations
        deal_results = f'{output["Product"][0]} Priced at: {output["Price"][0]}\n '\
        f'{output["Link"][0]} \n'\
        f'{output["Product"][1]} Priced at: {output["Price"][1]}\n '\
        f'{output["Link"][1]} \n'\
        f'{output["Link"][2]} \n'f'{output["Product"][2]} Priced at: {output["Price"][2]}\n '\
        f'{output["Link"][2]} \n'\
        f'{output["Product"][3]} Priced at: {output["Price"][3]}\n '\
        f'{output["Link"][3]} \n'\
        f'{output["Product"][4]} Priced at: {output["Price"][4]}\n '\
        f'{output["Link"][4]} \n'
        return f'Did someone say they needed a deal on {item}, Full Results: {deal_search.full_url()}? \n {deal_results}'
    except AttributeError:
        #attribute error is used on the off chance nothign appears for the search item.
        return f'sorry my guy, i couldn\'t find any deals for {item} 😕'

def audio_message(message,gear = None, price = None, quant = None):
    inputls = message.content.split(' ')
    #list splicing to acocunt for the fact that users may not always specify None for input
    try:
        if len(inputls) == 3:
            gear = inputls[1]
            price = int(inputls[2])
            quant = None
        elif len(inputls) == 4:
            gear = inputls[1]
            price = int(inputls[2])
            quant = int(inputls[3])
        #based on length adjust input value accordingly and pass through AudiophileGear module
        hardware_search = audiophile.AudiophileGear(gear,price,quant)
        hardware_search.gear_search()
        hardware_search.morph_search()
        hardware_search.filter_search()
        hardware_results = hardware_search.print_results()
        #output with results
        return hardware_results
    except:
        return
