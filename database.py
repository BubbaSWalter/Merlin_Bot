# database.py
# Description: place to store datafiles
# Created by: BubbaSWalter
# Version: 1.0.0.0 A
import os
import sqlite3
pwd = os.path.dirname(os.path.realpath(__file__))


async def conntodb():
    exists = os.path.isfile(pwd + "\\data\\commands.db")
    if not exists:
        conn = sqlite3.connect(pwd + "\\data\\commands.db")
        # Table Commands
        #   ComName, PermLevel, Output
        conn.execute('''CREATE TABLE "commands" ("ComName" text, "ComPerm" text, 
            "ComOutput" text, PRIMARY KEY("Comname"))''')
        conn.commit()
        conn.close()
    exists = os.path.isfile(pwd + "\\data\\points.db")
    if not exists:
        conn = sqlite3.connect(pwd + "\\data\\points.db")
        conn.execute('''CREATE TABLE points
                 (PointUser text, PointsMana, PointsExp, PRIMARY KEY("PointUser"))''')
        conn.commit()
        conn.execute('''CREATE TABLE editors
                 (PointUser text)''')
        conn.commit()
        conn.close()
    exists = os.path.isfile(pwd + "\\data\\quotes.db")
    if not exists:
        conn = sqlite3.connect(pwd + "\\data\\quotes.db")
        # Table Quotes
        #   QuoteID, WHo Quoted, Who being Quoted, Game WHere Quote Happened, Time, Quote,
        conn.execute('''CREATE TABLE quotes
                 (QuoteQuoter text, 
                 QuoteTarget text, QuoteGame text, 
                 QuoteDate text, QuoteQuote text)''')
        conn.commit()
        conn.close()
    exists = os.path.isfile(pwd + "\\data\\queue.db")
    if not exists:
        conn = sqlite3.connect(pwd + "\\data\\queue.db")
        conn.execute('''CREATE TABLE queue
                 (QueueName PRIMARY KEY, QueueDate text)''')
        conn.commit()
        conn.close()
    exists = os.path.isfile(pwd + "\\data\\settings.db")
    if not exists:
        conn = sqlite3.connect(pwd + "\\data\\settings.db")
        conn.execute('''CREATE TABLE hashtags
                     (name text, value text, PRIMARY KEY("name"))''')
        conn.commit()
        conn.execute('''CREATE TABLE points
                     (name text, value text, PRIMARY KEY("name"))''')
        conn.commit()
        conn.execute('''CREATE TABLE pastebins
                     (name text, value text, PRIMARY KEY("name"))''')
        conn.commit()
        conn.close()



