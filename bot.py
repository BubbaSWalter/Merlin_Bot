# start.py
# Description: Starting file for Merlin_b0t
# Created by: BubbaSWalter
# Version: 2.0.0.0 A
import _thread
import re
import cfg
import websockets
import time
import utils
import bleach
import commands_custom
import commands_static
from time import sleep
import alerts


async def bot():
    async with websockets.connect(f'{cfg.HOST}:{cfg.PORT}', ssl=True) as s:
        await s.send(f"PASS {cfg.PASS}")
        await s.send(f"NICK {cfg.HOST}")
        await s.send(f"CAP REQ :twitch.tv/membership twitch.tv/tags twitch.tv/commands")
        await s.send(f"JOIN #{cfg.CHAN}")
        _thread.start_new_thread(utils.generateviewerlist, ())
        cfg.sock = s
        print("Merlin_b0t Connected")
        while True:
            try:
                incoming = str(await s.recv()).strip()
                if "PING :tmi.twitch.tv" in incoming:
                    await s.send("PONG :tmi.twitch.tv")
                else:
                    await(messagehandler(s, incoming))
                try:
                    await utils.chatmessage(s, cfg.alerts[0], None)
                    cfg.alerts.pop(0)
                except:
                    if 1 > 2:
                        print()
            except websockets.ConnectionClosed as e:
                print(e)
                sleep(3)
                s = websockets.connect('wss://irc-ws.chat.twitch.tv:443', ssl=True)
                await s.send(f"PASS {cfg.PASS}")
                await s.send(f"NICK {cfg.HOST}")
                await s.send(f"CAP REQ :twitch.tv/membership twitch.tv/tags twitch.tv/commands")
                await s.send(f"JOIN #{cfg.CHAN}")
                cfg.sock = s
            if cfg.cnt == 0:
                cfg.cnt = 1
                _thread.start_new_thread(alerts.start, ())


async def messagehandler(s, incoming):
    # print(incoming)
    if 'HOSTTARGET' in incoming:
        rehost = re.compile(r"\s:(\w*)")
        host = re.search(rehost, incoming).group(1)
        print(f'Now Hosting {host}')
    if 'PRIVMSG' in incoming:
        await privmsg(s, incoming)
    if 'WHISPER' in incoming:
        await whisper(s, incoming)


async def whisper(s, incoming):
    print(incoming)
    # @badges=bits-charity/1;color=#008000;display-name=BubbaSWalter
    # ;emotes=;message-id=203;thread-id=37816957_108944853;turbo=0
    # ;user-id=37816957;user-type=
    # :bubbaswalter!bubbaswalter@bubbaswalter.tmi.twitch.tv WHISPER bubbas_bot :Hello Bot
    redisplayname = re.compile(r";display-name=(\w*);")
    remessage = re.compile(fr'{cfg.USER}\s:([\s\S]+)')
    displayname = re.search(redisplayname, incoming).group(1)
    username = displayname.lower()
    message = re.search(remessage, incoming).group(1)
    usermode = 0
    for p in range(0, len(cfg.viewerList)):
        # print(cfg.viewerList[p])
        user = cfg.viewerList[p].split('||')[0]
        usertype = cfg.viewerList[p].split('||')[1]
        if displayname.lower() in user:
            if 'moderators' in usertype or 'moderators' in usertype or\
                    'moderators' in usertype or 'moderators' in usertype:
                usermode = 4
            if 'editor' in usertype:
                usermode = 5
            if 'broadcaster' in usertype:
                usermode = 6
    if message[0] == '!':
        response = await commands_custom.command(username, usermode, message)
        if not response:
            response = await commands_static.commands(username, usermode, message)
        if response:
            response = commandsVars(response)
            await utils.chatmessage(s, f'/w {username} {response}', None)
    formattedmessage = f'{time.strftime("%I:%M %p", time.localtime(time.time()))}' \
        f' {usermode} {displayname}: {message}'
    print(formattedmessage)

async def privmsg(s, incoming):
    # print(cfg.chatmess)
    redisplayname = re.compile(r";display-name=(\w*);")
    retmitimestamp = re.compile(r";tmi-sent-ts=(\d*);")
    remsgid = re.compile(r";id=(.+?);")
    reusername = re.compile(r":(\w*)!")
    rebadges = re.compile(r';badges=([\s\S]*);c')
    remessage = re.compile(fr'#wizardsrwe\s:([\s\S]+)')

    usermode = 1
    username = re.search(reusername, incoming).group(1)
    displayname = re.search(redisplayname, incoming).group(1)
    badges = re.search(rebadges, incoming).group(1)
    # Regular to be established after points integration
    if 'subscriber' in badges:
        usermode = 3
    if 'global_mod' in badges:
        usermode = 4
    elif 'moderator' in badges:
        usermode = 4
    elif 'staff' in badges:
        usermode = 4
    elif 'admin' in badges:
        usermode = 4
    for item in cfg.editors:
        if displayname.lower() in item:
            usermode = 5
    if 'broadcaster' in badges:
        usermode = 6
    msgid = re.search(remsgid, incoming).group(1)
    msgtimestamp = int(re.search(retmitimestamp, incoming).group(1)) / 1000
    msgtime = time.strftime("%I:%M %p", time.localtime(msgtimestamp))
    message = re.search(remessage, incoming).group(1)
    message = bleach.clean(message)
    if usermode < 4:
        test = await utils.linkdetection(message)
        if test:
            test = await utils.permitcheck(displayname.lower(), time)
            if test:
                await utils.deletemessage(s, msgid, username, 'link', msgtimestamp)
        reemoji = re.compile('(\u00a9|\u00ae|[\u2000-\u3300]|\ud83c[\ud000-\udfff]|'
                             '\ud83d[\ud000-\udfff]|\ud83e[\ud000-\udfff])')
        if re.search(reemoji, message) in message:
            count = len(re.findall(reemoji, message))
            await utils.deletemessage(s, msgid, username, 'sym', msgtimestamp)
        respeical = re.compile("[!@#$%^&*(),.?\":{}|<>_\\\=\[\];`~+'/\-]")
        if re.search(respeical, message):
            count = len(re.findall(respeical, message))
            if count > 30:
                await utils.deletemessage(s, msgid, username, 'sym', msgtimestamp)
    if message[0] == '!':
        response = await commands_custom.command(username, usermode, message)
        if not response:
            response = await commands_static.commands(username, usermode, message)
        if response:
            command = message[1:].split(' ')[0].strip()
            test = False
            cooldowntime = 0
            for p in range(0, len(cfg.cooldownList)):
                if command in cfg.cooldownList[p].split(',')[0]:
                    if float(cfg.cooldownList[p].split(',')[1]) > msgtimestamp:
                        test = True
                        cooldowntime = cfg.cooldownList[p].split(',')[1]
                    if float(cfg.cooldownList[p].split(',')[1]) < msgtimestamp:
                        cfg.cooldownList.pop(p)
            if not test:
                cfg.cooldownList[len(cfg.cooldownList)] = f'{command},{msgtimestamp + 60}'
                response = commandsVars(response)
                await utils.chatmessage(s, response, None)
            if test:
                cooldowntimer = int(round(float(cooldowntime) - float(msgtimestamp), 0))
                response = f'@{displayname} => Command !{command} is on cooldown for {cooldowntimer} seconds'
                await utils.chatmessage(s, response, None)
    formattedmessage = f"{msgtime} {usermode} {displayname}: {message.strip()}"
    print(formattedmessage)


async def userstate(s,incoming):
    #> @badge-info=;badges=staff/1,broadcaster/1,turbo/1;color=#008000;display-name=ronni;emotes=
    # ;id=db25007f-7a18-43eb-9379-80131e44d633;login=ronni;mod=0;msg-id=resub;msg-param-cumulative-months=6
    # ;msg-param-streak-months=2;msg-param-should-share-streak=1;msg-param-sub-plan=Prime
    # ;msg-param-sub-plan-name=Prime;room-id=1337;subscriber=1;system-msg=ronni\shas\ssubscribed\sfor\s6\smonths!;tmi-sent-ts=1507246572675;turbo=1;user-id=1337;user-type=staff :tmi.twitch.tv USERNOTICE #dallas :Great stream -- keep it up!
    redisplayname = re.compile(r";display-name=(\w*);")

def commandsVars(output):
    reGameLookup = re.compile('\$game\((w+)\)')
    if re.search(reGameLookup, output):
        holder = re.search(reGameLookup, output)
        holder = commands_static.twitchapi(chan_name=holder, request_type='game')
        output = re.sub(reGameLookup, holder, output)
    reGameLookup = re.compile('\$status\((w+)\)')
    if re.search(reGameLookup, output):
        holder = re.search(reGameLookup, output)
        holder = commands_static.twitchapi(chan_name=holder, request_type='status')
        output = re.sub(reGameLookup, holder, output)
    reGameLookup = re.compile('\$status\((w+)\)')
    if re.search(reGameLookup, output):
        holder = re.search(reGameLookup, output)
        holder = commands_static.twitchapi(chan_name=holder, request_type='url')
        output = re.sub(reGameLookup, holder, output)
    return output
