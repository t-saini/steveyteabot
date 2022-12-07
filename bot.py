#bot.py
#https://betterprogramming.pub/coding-a-discord-bot-with-python-64da9d6cade7

import discord
import threading
import time
import datetime
import bot_interactions
import utility
import web_scanning


setup = utility.run_ini()
DISCORD_TOKEN = setup['token']['value']
intents = discord.Intents.default()
intents.members = True
bot = discord.Client()

def posh_check():
    ground_truth = web_scanning.find_posh()
    logger.info('Established Initial Ground Truth for Posh Mart')
    while True:
        time.sleep(1800)
        new_truth = web_scanning.find_posh()
        try:
            if ground_truth != new_truth:
                new_listings = list(set(new_truth).difference(set(ground_truth)))
                dev_channel = bot.get_channel(int(setup['IMBREGAR']['channel_id']))
                for listing in new_listings:
                    bot.loop.create_task(dev_channel.send(f'{listing}'))
                ground_truth = new_truth
        except:
            dev_channel = int(setup['dev_server']['bot-logs'])
            bot.loop.create_task(dev_channel.send(f'Failed to check posh mart'))


def dapper_check():
    latest_article = []
    logger.info('Established Initial Ground Truth for Dappered')
    while True:
        time.sleep(.001)
        time_now = datetime.datetime.now().strftime("%H:%M")
        time_to_work = ['09:15','12:30','15:30','18:30']
        if time_now in time_to_work:
            try:
                current_article = web_scanning.dapper_up()
                if current_article != latest_article:
                    new_article = list(set(current_article).difference(set(latest_article)))
                    channels_to_msg = [setup['dev_server']['channel_id'],
                    setup['DBR']['channel_id'], setup['IMBREGAR']['channel_id']]
                    for single_channel in channels_to_msg:
                        for article in new_article:
                            dev_channel = bot.get_channel(int(single_channel))
                            selected = utility.gen_random_int(bot_interactions.quips)
                            bot.loop.create_task(dev_channel.send(f'{bot_interactions.quips[selected]}\n{article}'))
                    latest_article = current_article
            except:
                dev_channel = setup['dev_server']['bot-logs']
                dev_channel.send(f'Failed the dapper check')


async def on_message(message):
    commands_in = {
        '!audio': bot_interactions.audio_message,
        '!deals': bot_interactions.deals_message,
        '!wiki': bot_interactions.wiki_message 
        }
    commands = {'!help': bot_interactions.help_message,
        '!tea': bot_interactions.quip_message}
    key_phrases = ['say the thing steveyt', 
    'say the thing stevey tea', 'say the thing steveytea']
    output = None
    try:
        if message.content.lower().split(' ')[0] in commands_in:
            user_input = message.content.lower().split(' ')[0]
            output = commands_in.get(user_input)(message)
        elif message.content.lower().split(' ')[0] in commands:
            command = message.content.lower().split(' ')[0]
            output = commands.get(command)()
        elif message.content.lower() in key_phrases:
            output = commands.get('!tea')()
        elif 'happy birthday' in message.content.lower():
            if message.author != bot.user:
                output = bot_interactions.birthday_message()
    except Exception as error:
        dev_channel = bot.get_channel(int(setup['dev_server']['bot-logs']))
        bot.loop.create_task(dev_channel.send(
            f'The following error occured\n{error}\n'\
            f'Could not handle the following: {message.content.lower()} from: {message.author}'
            ))
    if output == None:
        return
    await message.channel.send(output)

@bot.event
async def on_ready():
    #on connection
    guild_count = 0
    for guild in bot.guilds:
        #itterate through the number of servers/guilds that have gained access through the Auth2link
        try:
            logger.info(f'Connected-{guild.id} (name:{guild.name})')
            #print the name and guild id and add one to the counter
            guild_count += 1
        except:
            logger.warning(f'Connection Falure-{guild.id} (name:{guild.name})')
            if guild_count != 0:
                guild_count -= 1
        #print a message showing the total number of servers connected. Ths can be useful in the future if multiple amount of servers will be used.
    logger.info(f'Connected to {guild_count} servers, how neat.')
    try:
        logger.info('-Initializing thread 1-')
        t1 = threading.Thread(target = dapper_check)
        t1.setDaemon(True)
        logger.info('-Daemon Set for thread 1-')
        t1.start()
        logger.info('-Thread 1 for dapper monitoring complete!-')
    except:
        logger.warning('+Failed to create thread for dapper monitoring+')
    try:  
        logger.info('-Initializing thread 2-')
        t2 = threading.Thread(target = posh_check)
        t2.setDaemon(True)
        logger.info('-Daemon Set for thread 2-')
        t2.start()
        logger.info('-Thread 2 for posh monitoring complete!-')
    except:
        logger.warning('+Failed to create thread for posh monitoring+')
    while True:
        time.sleep(.001)
        msg = await bot.wait_for("message")
        await on_message(msg)


if __name__ == "__main__":
    #establishes connection
    logger = utility.system_logs()
    bot.run(DISCORD_TOKEN)
