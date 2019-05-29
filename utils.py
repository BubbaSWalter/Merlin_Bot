# utils.py
# Description: Bot Program
# Created by: BubbaSWalter
# Version: 1.0.0.0 A
import re
import requests
import asyncio
import cfg
import json
from time import sleep


async def chatmessage(s, mess, extra):
    """
    Function: Chat
    Description: Send Chat Messages
    :param s: socket to send message
    :param mess: message to send
    :param extra: Used to explain why a Timeout, Ban or Message Deletion was used
    :return: Nothing
    """

    if extra:
        await s.send(f'PRIVMSG #{cfg.CHAN} :{mess}')
        await s.send(f'PRIVMSG #{cfg.CHAN} :{extra}')
    if not extra:
        await s.send(f'PRIVMSG #{cfg.CHAN} :{mess}')
    await asyncio.sleep(cfg.LIMIT)


async def ban(sock, user):
    """
    Function: Ban
    Description: Ban Users
    ##Bot Needs to be MOD
    :param sock: socket to send message
    :param user: user to ban
    """

    await chatmessage(sock, f"/ban {user}", None)
    print(f"{cfg.USER}: BANNED {user}")


async def timeout(sock, user, seconds=600):
    """
    Function: Timeout
    Description: timeout Users
    ##Bot Needs to be MOD
    :param sock: socket to send message
    :param user: user to timeout
    :param seconds: seconds to timeout a user
    """
    await chatmessage(sock, f"/timeout {user} {seconds}", None)
    print(f"{cfg.USER}: Timeout {user} {seconds} seconds")


async def deletemessage(sock, msgid, user, issue,time):
    reason = ""
    if 'link' in issue:
        reason = f"WARNING @{user} You need to ask for permission before posting a link"
    if 'sym' in issue:
        reason = f"WARNING @{user} You have my attention now not sure if thats a good thing"
    test = False
    for p in range(0, len(cfg.issueList)):
        user = cfg.issueList[p].split('||')[0]
        probationtime = cfg.issueList[p].split('||')[1]
        if float(probationtime) > float(time):
            await chatmessage(sock,f"@{user} you win a 10 minute break for not following the rules", None)
            await timeout(sock, user, 600)
        if not float(probationtime) > float(time):
            cfg.issueList[len(cfg.issueList)] = f'{user}||{int(time) + 300}'
            await chatmessage(sock, f"/delete {msgid}", f"@{user} You need to ask for permission before posting a link")
    print("I Have Deleted a Message")


async def permitcheck(user,time):
    for i in range(0, len(cfg.permituser)):
        if user in cfg.permituser[i]:
            if time < cfg.permittime[i]:
                return False
            elif time > cfg.permittime[i]:
                return True


async def linkdetection(mess):
    """
    Check for Links, Returns True if there are Links
    :param mess:
    :return: True if there are Link Else returns False
    """
    check = (r'((([A-Za-z]{3,9}:(?:\/\/)?)(?:[-;:&=\+\$,\w]+@)?[A-Za-z0-9.-]+|(?:www.|[-;:&=\+\$,\w]+@)'
             r'[A-Za-z0-9.-]+)((?:\/[\+~%\/]*)?\??(?:[-\+=&;%@.\w_]*)#?(?:[\w]*))?)|(\d*\.\d*\.\d*\.\d*)|'
             r'((\w*\.)(asia|biz|co|com|edu|gov|info|int|jobs|live|net|me|org|tv|web|website|as|ca|cn|cu|de|fr|'
             r'iq|ir|it|us)'
             r'(\s|\.|$))')
    urls = re.search(check, mess)
    if urls:
        urls = urls.group(0)
        print(f'Urls Detected. Url:"{urls}"')
        return True
    if not urls:
        return False


def generateviewerlist():
    """
    Generate Operator List and Viewer List
    Should be called on a different thread
    """
    # opList{}, viewer{}
    while True:
        try:
            url = f"http://tmi.twitch.tv/group/user/{cfg.CHAN}/chatters"
            headers = {}
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                holder = json.loads(response.content)['chatters']
                cfg.viewerList.clear()
                for p in holder['broadcaster']:
                    cfg.viewerList[len(cfg.viewerList)] = f"{p}||broadcaster"
                for p in holder['staff']:
                    cfg.viewerList[len(cfg.viewerList)] = f"{p}||staff"
                for p in holder['admins']:
                    cfg.viewerList[len(cfg.viewerList)] = f"{p}||admin"
                for p in holder['global_mods']:
                    cfg.viewerList[len(cfg.viewerList)] = f"{p}||global_mods"
                for p in holder['moderators']:
                    cfg.viewerList[len(cfg.viewerList)] = f"{p}||moderators"
                for p in holder['vips']:
                    cfg.viewerList[len(cfg.viewerList)] = f"{p}||vips"
                for p in holder['viewers']:
                    cfg.viewerList[len(cfg.viewerList)] = f"{p}||viewers"
                for p in cfg.editors:
                    cfg.viewerList[len(cfg.viewerList)] = f"{p}||editor"
            else:
                print(f"[!] HTTP {response.status_code} calling [{url}]")
        except Exception as inst:
            print(type(inst))  # the exception instance
            print(inst.args)  # arguments stored in .args
            print(inst)  # __str__ allows args to be printed directly,
        sleep(5)
