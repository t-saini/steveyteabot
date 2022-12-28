# steveyteabot
We all have that friend that friend who is fashionable, is a tech head, and always somehow finds the best deals. The purpose of this bot is to encapsulate that friend into a Discord Bot using Python. This project originally started at the height of the pandemic.
<br />
This fetches information inputted by users regarding headphones, latest deals for online shopping, and wikipedia entries using APIs and Python libraries.
<br />
Additionally unique webscrappers were written to monitor online market places and blogs for new posts. Set with a timely interval, when a new item/post is dedicated it will alert the dedicated channels.
<br />
All python error messages are forwarded to an independent channel titled 'bot-logs'
<br />
<br />

File hierarchy:

bot.py<br />
|_ utility.py<br />
|_ web_scanning.py<br />
|_ bot_interactions.py<br />
&emsp;|_ audiophile.py<br />
&emsp;|_ slickdeals.py


Requirements:
<br />
requests==2.21.0 
<br />
pandas==1.3.1 
<br />
wikipedia==1.4.0 
<br />
discord.py==1.7.3
<br />
beautifulsoup4==4.9.3
<br />
discord==1.7.3

You will also need the lxml library if it is not already installed.
Linux users may run into a Pandas error when trying to run the bot.

Use case examples when the bot is a Discord Member:

Finding deals on Klipsch Spekaers
```
!deals Klipsch Speakers
```

Finding deals on iems/headphones at no higher than $200 USD
```
!audio iems 200
```

```
!audio headphones 200
```

Wikipedia seach

```
!wiki Godzilla
```
