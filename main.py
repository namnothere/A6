import discum
from discum.RESTapiwrap import *
import json
# from discum.RESTapiwrap import *
import datetime
import random
import os
import time
from dotenv import load_dotenv


load_dotenv()  #load .env file

from keep_alive import keep_alive

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN_6")
count4 = 0
rest_time = None
# channel_id = int(os.getenv("channel_ID"))
bot_ID = int(os.getenv("bot_ID"))

nem = "408957019794440192"

avoid_list = ['bot', 'b0t', 'bOt', 'BOT', 'b4t', 'copy', 'paste', 'p4ste', 'c0py', 'kill', 'k1ll', 'gay', 'trans', 'transgender', 'lgbt', 'nigga', 'nibba', 'black', 'fuck', 'fuk', 'fk', 'catch bot', 'catch b0t','bots', 'b0ts']
# bot = commands.Bot(
  # command_prefix=commands.when_mentioned_or('$$'), self_bot=True)
bot = discum.Client(token=DISCORD_TOKEN, log = False)



@bot.gateway.command
def helloworld(resp):
  if resp.event.ready_supplemental: #ready_supplemental is sent after ready
    user = bot.gateway.session.user
    print("Logged in as {}#{}".format(user['username'], user['discriminator']))
    


@bot.gateway.command
def msg(resp):
  if resp.event.message:
    global count4
    global rest_time
    user = bot.gateway.session.user
    message = resp.parsed.auto()

    now = datetime.datetime.now()
    
    if user['id'] in (user_id['id'] for user_id in message["mentions"]):
      bot.sendMessage("601809454392016916" , f"<@{nem}>\nReceived a message\nMessage content: ```{message['content']}```\nMessage ID: {message['id']}")
      return

    if now.hour < 18 or sleep(rest_time):
      return

    if message["author"]["id"] == str(bot_ID) and message["embeds"]:
      # print(message["embeds"][0])
      # print(bot.getMessage(message['channel_id'], message['id']))
      t = datetime.datetime.now()
      for embed in message["embeds"]:
        d = embed
        try:
          if d['footer']['text'] != 'Ends' or '$0.00' in d['description']:
            return
            
          print(d)
          
          end = datetime.datetime.fromisoformat(d['timestamp'][:-6])
          start = int(((end - t)/4).total_seconds())
          stop = ((end - t)/2 + datetime.timedelta(seconds=0.5)).total_seconds()

          print("start: ", start)
          print("stop: ", stop)
          if stop < 2:
            t = stop - 0.2
          else:
            t = (random.randrange(start, int(stop)) + (random.randrange(0, 9))/10)
          amount = ((d['description']).partition('\xa0')[2])[0:5]
          if "$" not in amount:
            amount = "$0.00"
          print(f'amount: {amount}')
          if 'An airdrop appears' in d['title']:
            count4 += 1
            if int(amount[1]) > 0:
              t = 2.8
            time.sleep(t)
            
            msg = ((bot.getMessage(message['channel_id'], message['id'])).json())[0]

            for reaction in msg['reactions']:
              check = reactions(message['id'],message['channel_id'], reaction['emoji']['name'])
              if check:
                emoji = reaction['emoji']['name']
                bot.addReaction(message['channel_id'], message['id'], emoji)
                print(f"Reaction added to an airdrop - {t}s - {user['username']} - bot 4")

          elif 'A red packet appeared' in d['title']:
            count4 += 1
            
            wait = (stop - start)/2 + 0.1
            if wait > 7:
              wait = 3 + random.random()
            if int(amount[1]) > 0:
              wait = 0.24
            time.sleep(wait)
            msg = ((bot.getMessage(message['channel_id'], message['id'])).json())[0]
            
            for reaction in msg['reactions']:
              check = reactions(message['id'],message['channel_id'], reaction['emoji']['name'])
              print(check)
              if check:
                emoji = reaction['emoji']['name']
                bot.addReaction(message['channel_id'], message['id'], emoji)
                print(f"Reaction added to a red packet - {wait}s - {user['username']} - bot 4")
                
          elif 'started a phrase drop!' in d['description']:
            count4 += 1
            ph = (((d['description']).partition('**The phrase is:** ')[2])
            [1:-1]).replace('\u200b', '')
            print(f"Phrase: {ph}")    
            if any(map(ph.__contains__, avoid_list)):
              print('bot detected')
              return
            elif " " not in ph and len(ph) > 9:
              return
            t = len(ph)
            if (t < 10):
              r = 3.5
            else:
              time.sleep(start)
              r = t/10 + t - start
            bot.typingAction(message['channel_id'])
            
            delay(r)
            bot.sendMessage(message['channel_id'], ph)
            
            print(f"Successfully sent the message - {r}s - {user['username']} - bot 4")
          if (count4 + random.randrange(0, 2) > 7):
            rest = random.randrange(600, 900)
            print(f'Reach maximum of airdrops catch. Sleep for {rest} seconds - bot 4')
            count4 = 0
            delay(rest)
            print("Finish sleeping")
        except KeyError:
          pass
        except Exception as e:
          print(f"Error while trying to react - {e} - bot 4")
  

def reactions(message_id, channel_id, emoji):  
  url = f'https://discord.com/api/v9/channels/{channel_id}/messages/{message_id}/reactions/{emoji}?limit=100'
  s = bot.s
  r = s.get(url, headers = s.headers)
  #decompression; gzip/deflate is automatically handled by requests module
  if r.headers.get('Content-Encoding') == "br":
    import brotli
    r._content = brotli.decompress(r.content)
  data = json.loads(r.content)  
  #check if bot is in data
  if str(bot_ID) in (element['id'] for element in data):
    return True
  return False

def sleep(rest):
  now = datetime.datetime.now()
  #if it not pass the rest time or rest is None as default
  if now < rest or not rest:
    return False
  return True

# def status():
#   sts = ['Eating', 'Deadline', 'HAACHAMA COOKING']
#   i = 0
#   while True:
#     if i >= len(sts):
#       i = 0
#     bot.gateway.setCustomStatus(sts[i])
#     time.sleep(5)
#     i += 1

thread = keep_alive()
bot.gateway.run(auto_reconnect=True)


