#!/usr/bin/env python3

from telethon import TelegramClient, events
import os
import configparser

config_file = os.path.join(os.path.expanduser("~"), ".telegram_dissuader.conf")

configs = configparser.ConfigParser()
if os.path.exists(config_file):
    configs.read(config_file)

configs_edited = False

if not "telegram_api" in configs:
    configs.add_section("telegram_api")
    print("Please visit https://my.telegram.org and obtain a Developer API Key first..")
    print("Input the API Key details")
    configs["telegram_api"]["api_id"] = input("api_id: ")
    configs["telegram_api"]["api_hash"] = input("api_hash: ")
    configs_edited = True

if not "vocal_harassment" in configs:
    configs.add_section("vocal_harassment")
    configs["vocal_harassment"]["response"] = input("Please input the default response: ")
    configs["vocal_harassment"]["whitelist"] = input("Please input the list of names to whitelist (separated by spaces): ")
    configs_edited = True

if configs_edited:
    with open(config_file, 'w') as cfile:
        configs.write(cfile)
    print("If you need to change those values edit file the config file: {}".format(config_file))

whitelist = configs["vocal_harassment"]["whitelist"].split()

client = TelegramClient("vocal harassment dissuader", configs["telegram_api"]["api_id"], configs["telegram_api"]["api_hash"], spawn_read_thread=False, update_workers=1)
client.start()

myself = client.get_me()

print("Whitelisted users:")
for w in whitelist:
    print(w)

@client.on(events.NewMessage(incoming=True))
def on_new_message(event):
    global myself
    try:
        dest = event.message.to_id
        if dest.user_id == myself.id:
                dest = event.message.from_id
        if event.message.message is not None:
            if "cracco" in event.message.message.lower():
                try:
                    client.send_message(dest, "chiiii?")
                except:
                    pass
        sender = event.sender
        if sender is not None and sender.username not in whitelist and sender.first_name not in whitelist and sender.id not in whitelist:
            for a in event.message.document.attributes:
                if a.voice:
                    #print("received voice message from {} {} {} ({})".format(sender.username, sender.firts_name, sender.id, sender))
                    client.send_message(dest, configs["vocal_harassment"]["response"])
                    break
    except:
        pass

client.idle()
