# cfg.py
# Description: Contains static commands
# Created by: BubbaSWalter
# Version: 1.0.0.0 A
import cfg
import datetime
import json
import os
import random
import sqlite3
import time
import urllib.request
import urllib.parse
import urllib.error
import requests
import database
import hashlib


async def commands(displayname, usermode, message):
    user = displayname.lower().strip()
    message = message.strip()
    command = message.split(' ')[0][1:].lower()
    params = message[len(command) + 1:]
    if "game" in command:  #
        if usermode > 3 and params:
            return f'@{user} => game updated to {updatetwitchapi(cfg.CHAN, "game", params)}'
        game = twitchapi(cfg.CHAN, 'game')
        return f"@{user} the current game is {game}"
    elif "title" in command:
        if usermode > 3 and params:
            f'@{user} => title updated to {updatetwitchapi(cfg.CHAN, "status", params)}'
        status = twitchapi(cfg.CHAN, 'status')
        return f"@{user} the current title is {status}"
    elif "uptime" in command:
        return getuptime()
    elif "followtime" in command:
        return getfollowing(user)
    elif "permit" in command:
        return permitsgive(user, usermode, params)
    elif "quote" in command:
        holder = params[0:].strip().split(' ')
        message = ""
        for item in holder[0:]:
            message += f' {item}'
        message = message.strip()
        return await processquotes(displayname, usermode, message)
    elif 'spells' in command or 'commands' in command or 'cmdlist' in command:
        return f'Hey I am Merlin_bot I have many commands which can be found here => {proccesscommands()}'
    elif 'poll' in command and usermode > 3:
        processpoll(params)
    elif "quit" in command and usermode >= 5:
        exit()
    else:
        return ""


def getuserid(chan_name):
    try:
        url = f"https://api.twitch.tv/kraken/users?login={chan_name}"
        heading = {
            "Client-ID": cfg.CLIENT_ID,
            'Accept': 'application/vnd.twitchtv.v5+json',
        }
        req = urllib.request.Request(url, headers=heading)
        resp = urllib.request.urlopen(req)
        output = json.loads(json.dumps(json.loads(resp.read())['users'][0]))
        return output['_id']
    except urllib.error as e:
        print('getuserid', e)
        return e
    except Exception as e:
        print('getuserid', e)
        return e


def twitchapi(chan_name, request_type):
    try:
        chan_id = getuserid(chan_name)
        url = f"https://api.twitch.tv/kraken/channels/" + str(chan_id)
        heading = {
            "Client-ID": cfg.CLIENT_ID,
            'Accept': 'application/vnd.twitchtv.v5+json'
        }
        req = urllib.request.Request(url, headers=heading)
        response = urllib.request.urlopen(req)
        output = json.loads(response.read())[request_type]
        return output
    except urllib.error as e:
        print('getgame', e)
        return e
    except Exception as e:
        print('getgame', e)
        return e


def updatetwitchapi(chan_name, update_type, params):
    try:
        chan_id = getuserid(chan_name)
        url = f"https://api.twitch.tv/kraken/channels/" + str(chan_id)
        heading = {
            "Client-ID": cfg.CLIENT_ID,
            'Accept': 'application/vnd.twitchtv.v5+json',
            'Authorization': f'OAuth {cfg.AUTH_USER}'
        }
        stuff = {"channel": {f"{update_type}": f"{params.strip()}"}}
        r = requests.put(url=url, json=stuff, headers=heading)
        response = json.loads(json.dumps(r.content.decode()))
        return response
    except Exception as e:
        print('getstutus', e)
        return e


def getuptime():
    try:
        url = f"http://decapi.me/twitch/uptime/{cfg.CHAN}"
        req = urllib.request.Request(url)
        response = urllib.request.urlopen(req)
        output = response.read().decode()
        return output
    except urllib.error as e:
        print('getuptime', e)
        return e
    except Exception as e:
        print('getuptime', e)
        return e


def getfollowing(user):
    try:
        url = f"http://decapi.me/twitch/followage/{cfg.CHAN}/{user}"
        req = urllib.request.Request(url)
        response = urllib.request.urlopen(req)
        output = response.read().decode()
        return output
    except urllib.error as e:
        print('getfollowing', e)
        return e
    except Exception as e:
        print('getfollowing', e)
        return e


def apiaccess(string):
    try:
        url = string
        r = requests.post(url=url)
        response = json.loads(json.dumps(r.content.decode()))
        return response
    except Exception as e:
        print(e)


def permitsgive(user, usermode, params):
    if usermode > 3 and len(params) > 0:
        print(params)
        print("Permit Process Started")
        stamp = time.time() + 60
        count = len(cfg.permittime)
        print(count)
        cfg.permittime[count] = stamp
        cfg.permituser[count] = params.strip().lower()
        print(f'"{cfg.permituser}" "{cfg.permittime}"')
        return f"@{user} has 60 seconds to post one link"


def processquotes(user, usermode, message):
    """
    :param user:
    :param usermode:
    :param message:
    :return:
    """
    holding = message.split(' ')
    pwd = os.path.dirname(os.path.realpath(__file__))
    conn = sqlite3.connect(pwd + "\\data\\quotes.db")
    cur = conn.cursor()
    if ' add ' in holding[0] and usermode > 3:
        try:
            game = twitchapi(chan_name=cfg.CHAN, request_type='game')
            quoteduser = holding[1]
            quote = ""
            for i in range(2, len(holding)):
                quote += f" {holding[i]}"
            now = datetime.datetime.now()
            date = f"{now.month}-{now.day}-{now.year}"
            output = f'@{user} Quote Added -> {quoteduser} "{quote}" - {game} {date}'
            sql = f"INSERT INTO quotes (QuoteTarget, QuoteQuoter, QuoteGame,QuoteDate,QuoteQuote ) " \
                f"VALUES('{quoteduser}','{user}','{game}','{date}','{quote}')"
            conn.execute(sql)
            conn.commit()
            conn.close()
            return output
        except sqlite3.Error as e:
            output = f"Database error:{e}"
            conn.close()
            return output
        except Exception as e:
            output = f"Exception in _query: {e}"
            conn.close()
            return output

    if ' del ' in holding[0] and usermode > 3:
        try:
            if len(holding[1]) > 0:
                sql = f"DELETE from quotes WHERE ROWID = {holding[1]}"
                conn.cursor().execute(sql)
                conn.close()
                output = f'@{user} Quote#{holding[1]}'
                return output
        except sqlite3.Error as e:
            output = f"Database error:{e}"
            conn.close()
            return output
        except Exception as e:
            output = f"Exception in _query: {e}"
            conn.close()
            return output

    else:
        try:
            cur.execute("SELECT COUNT(*) from quotes")
            rows = cur.fetchall()
            rowid = rows[0][0]
            print(rowid)
            if rowid > 1:
                value = random.randrange(1, rowid, 1)
            elif rowid == 0:
                return
            else:
                value = 1
            cur.execute(f"SELECT * FROM quotes where ROWID = {value}")
            rows = cur.fetchall()
            output = ""
            for item in rows:
                output = f'Quote#{value} {item[1]}"{item[4].strip()}"-' \
                    f' {item[2]} {item[3]} Quoted By:{item[0]}'
            conn.close()
            return output
        except sqlite3.Error as e:
            output = f"Database error:{e}"
            conn.close()
            print(output)
            return output
        except Exception as e:
            output = f"Exception in _query: {e}"
            conn.close()
            print(output)
            return output


def processpoll(params):
    data1 = {}
    options = []
    test = params.split('||')[1].strip().split('|')

    for item in test:
        if not options:
            options = (item,)
        else:
            options = options + (item,)
    data1["title"] = params.split('||')[0].strip()
    data1["options"] = options
    data1["multi"] = False
    print(data1)
    r = requests.post('https://www.strawpoll.me/api/v2/polls', json=data1)
    print(f"https://www.strawpoll.me/{json.loads(r.content)['id']}")


def proccesscommands():
    holderstatic = {}
    holdercustom = {}
    holderstatic[0] = 'Game\tEverybody\tGet Current Stream Game however MOD can use it to update the game'
    holderstatic[1] = "uptime\tEverybody\tDisplays how long the stream has been live form"
    holderstatic[2] = "status\tEverybody\tGet Current Stream Title  however MOD can use it to update the title"
    holderstatic[3] = "quote\tEverybody\tDisplays a Quote"
    holderstatic[4] = "followtime\tEveryone\tDisplays how long you have followed the stream"
    holderstatic[5] = 'quote add\tModerator\tAdds Quote to bot !quote add Bubba This Cool  -> Quote#1 Bubba"' \
                      ' This is Cool"-Some Date Quoted By:BubbaSWalter'
    holderstatic[6] = "quote del\tModerator\tRemove Quote from bot ex: !quote del 12"
    holderstatic[7] = "permit\tModerator\tpermits a user to post 1 link expires in 60 seconds"
    holderstatic[8] = "poll\tModerator\tCreates a Poll ex:!poll IS This a Poll||Yes|No"
    conn = sqlite3.connect(database.pwd + "\\data\\commands.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM commands")
    rows = cur.fetchall()
    for row in rows:
        perms = row[1]
        if '-r' in perms:
            perms = 'Regular Viewers'
        if '-s' in perms:
            perms = 'Subscribers'
        if '-m' in perms:
            perms = 'Moderator'
        if '-kb' in perms:
            perms = 'editor'
        holdercustom[len(holdercustom)] = f'{row[0]}\t{perms}\t{row[2]}'
    conn.close()

    data = ""
    data += "Static Commands \r\n"
    data += "Command\tPermission Level\tOutput\r\n"
    for item in range(0, len(holderstatic)):
        data += f'!{holderstatic[item]}\r\n'
    data += "Custom Commands\r\n"
    data += "Command\tPermission Level\tOutput\r\n"
    for item in range(0, (len(holdercustom))):
        data += f'!{holdercustom[item]}\r\n'
    hash_string = hashlib.md5(data.encode())
    hash_string = hash_string.hexdigest()

    conn = sqlite3.connect(database.pwd + "\\data\\settings.db")
    cur = conn.cursor()
    cur.execute("SELECT count(*) FROM hashtags")
    rows = cur.fetchall()
    count = rows[0][0]
    hash_check = "0"
    if count != 0:
        cur.execute("SELECT * FROM hashtags")
        rows = cur.fetchall()
        for row in rows:
            if 'commands' in row[0]:
                hash_check = f'{row[1]}'
    if hash_string not in hash_check:
        conn = sqlite3.connect(database.pwd + "\\data\\settings.db")
        sql = f"REPLACE INTO hashtags('name', 'value') " \
            f"VALUES ('commands', '{hash_string}')"
        conn.execute(sql)
        conn.commit()
        paste_code = data
        paste_name = 'Merlin_bot Commands List'
        paste_private = 1
        paste_expire_date = '1D'
        url = "https://pastebin.com/api/api_post.php"
        holder = {'api_option': "paste", 'api_user_key': cfg.PASTEBIN_API_USER, 'api_paste_private': paste_private,
                  'api_paste_name': paste_name, 'api_dev_key': cfg.PASTEBIN_API, 'api_paste_code': paste_code,
                  'api_paste_expire_date': paste_expire_date}
        r = requests.post(url=url, data=holder)
        url = r.content.decode()
        sql = f"REPLACE INTO pastebins('name', 'value') " \
            f"VALUES ('commands', '{r.content.decode()}')"
        conn.execute(sql)
        conn.commit()
        conn.close()
        print(url)
        return url
    else:
        cur.execute("SELECT * FROM pastebins")
        rows = cur.fetchall()
        for row in rows:
            if 'commands' in row[0]:
                url = f'{row[1]}'
                print(url)
                return url
