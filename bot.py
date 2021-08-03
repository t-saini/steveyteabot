#bot.py
#https://betterprogramming.pub/coding-a-discord-bot-with-python-64da9d6cade7
#https://discord.com/api/oauth2/authorize?client_id=870489969574150194&permissions=259846011968&scope=bot

import os
from dotenv import load_dotenv
import discord
import random
import wikipedia_summary as wiki
import slickdeals as slick
import audiophile

'''
Main script for SteveyTea Bot. Uses wikipedia_summary, slickdeals, and audiophile imports for primary actions.
Discord library has the API, dotenv is needed to pull Discord_Token from .env file.
'''

load_dotenv('.env')

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
intents = discord.Intents.default()
intents.members = True

bot = discord.Client()

@bot.event
async def on_ready():
    #on connection
    guild_count = 0
    for guild in bot.guilds:
        #itterate through the number of servers/guilds that have gained access through the Auth2link
        print(f'Connected-{guild.id} (name:{guild.name})')
        #print the name and guild id and add one to the counter
        guild_count = guild_count + 1
        #print a message showing the total number of servers connected. Ths can be useful in the future if multiple amount of servers will be used.
    print(f'Bee Boop Bop Beep, SteveyTea is in, connected to {guild_count} servers, how neat.')



@bot.event
async def on_message(message):
    '''on_message was used for simplifying user experience in discord chat. Function contains full little quips for the bot and core functions'''
    welcome_messages = {0: 'H U L L O', 1: 'Hullo, anyone want tea?🐱‍👓', 2:'Yo I\'m trying to sleep', 3:'Where my brown bear at?'}
    tangisms = {0: 'expensive hot tea leaf juice...add black balls and asians will love you', 1: 'Yo I\'m trying to sleep', 2: 'you do be lookin kinda cute today' , 3: 'posture check mofucka'}
    ###Fun quips
    #
    if 'summon steveytea' in message.content.lower():
        #on message randomly select a welcome message from the welcome_messages dictionary
        response = random.randrange(len(welcome_messages))
        await message.channel.send(welcome_messages[response])

    if 'steveytea welcome' in message.content.lower():
        #bot will welcome a user one command.
        #future iteration will replace this with the on join function provided by the discord library
        name = message.content.split(' ')
        await message.channel.send(f'hullo {name[2]} 🐱‍👓')

    if 'thanks steveytea' in message.content.lower():
        #when a user thanks the bot, it will say you're welcome with the author's display name, not user name
        #the dispaly is the name users can actively change.
        await message.channel.send(f'youre welcome {message.author.display_name}')

    if 'happy birthday' in message.content.lower():
        #requires optimization, in that the bot wil continue to say happy birthday as long as other users say it.
        if message.author == bot.user:
        #this line of code prevents the bot from looping happy birthday forever.
            return
        else:
            await message.channel.send('HAPPY BIRTHDAY 🎈🎉🐱‍👓')
    #
    ###End fun quips

    if '!wiki' in message.content.lower():
        if message.author != bot.user:
            #if author isn't bot, pass message conent with !wiki replaced through wiki module
            start = wiki.WikipediaSummary(message.content.replace('!wiki',''))
            #message with url and alternative suggestions
            await message.channel.send(f'here\'s the sauce degens: {start.pagelookup()} , if this isn\'t what you wanted, i tried 🤷‍♂️ so, try one of those below. ')
            summarylist = str(start.suggestions()).replace(
                '[', '').replace(']', '')
            await message.channel.send(f'{summarylist}')

    if '!deals' in message.content.lower():
        item = message.content.lower().replace('!deals ', '')
        if message.author != bot.user:
            #if bot is not the author try to take the item metioned through slickdeals module
            try:
                deal_search = slick.SlickSearch(message.content)
                deal_search.crawl_search()
                deal_search.gen_deals()
                #message out with deal informations
                await message.channel.send(f'Did someone say they needed a deal on {item}, Full Results: {deal_search.full_url()}? \n {deal_search.display_deals()}')
            except AttributeError:
                #attribute error is used on the off chance nothign appears for the search item.
                await message.channel.send(f'sorry my guy, i couldn\'t find any deals for {item} 😕')

    if '!audio' in message.content.lower():
        if message.author != bot.user:
            inputls = message.content.split(' ')
            #list splicing to acocunt for the fact that users may not always specify None for input
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
            hardware_results = hardware_search.filter_search()
            #output with results
            await message.channel.send(f'Check it 😎 \n {hardware_results}')
    
    #I lied, more fun quips
    if '!tea' in message.content.lower():
        if message.author != bot.user:
            selected = random.randrange(len(tangisms))
            await message.channel.send(f'{tangisms[selected]}')

    if message.content.lower() == '!help':
        await message.channel.send('I\'m a simple bot modeled after the great Sleeping Dragon Steven Tang. You can use !wiki for Wikipedia searches and !deals for SlickDeals. !audio [price range] [how many results] to find some audiogear (example: !audio iems 200 5 | !audio headphones 300), Use !tea for some Steven Tangisms 🐱‍👓')


#establishes connection
bot.run(DISCORD_TOKEN)
