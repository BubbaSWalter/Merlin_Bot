# cfg.py
# Description: Contains Custom Commands
# Created by: BubbaSWalter
# Version: 1.0.0.0 A
import cfg
import sqlite3
import database


async def command(username, usermode, message):
    """
    Processes a Custom Command request
    :param username: User who Sent the Command
    :param usermode: Classification of User
    :param message: Message USer Sent
    :return: Send back output
    """
    user = username.lower()
    msg = message.lower()
    command = msg.split(' ')[0][1:]
    params = msg[len(command) + 1:]
    # User Mode
    # New User Mode 1
    # Regular User Mode 2
    # Subscriber Mode 3
    # Mod/GMod/Staff/Admin Mode 4
    # Editor Mode 5
    # Broadcaster Mode 6
    if usermode > 4 and "cmdadd" in command:
        # !cmdadd <cmdnamd> -permlevel || command
        output = ""
        if '||' in params:
            output = params.split('||')[1].strip()
        perms = ""
        comadd = params.split(' ')[1]
        async with sqlite3.connect(database.pwd + "\\data\\commands.db") as conn:
            try:
                async with conn.cursor() as cur:
                    cur.execute("SELECT * FROM commands")
                    rows = cur.fetchall()
                    for row in rows:
                        if comadd in row[0]:
                            lperms = row[1]
                            loutput = row[2]
                            if not output:
                                output = loutput
                            if '-r' in lperms:
                                perms = '-r'
                            if '-s' in lperms:
                                perms = '-s'
                            if '-m' in lperms:
                                perms = '-m'
                            if '-kb' in lperms:
                                perms = '-kb'
                conn.close()
            except sqlite3.Error as e:
                print("Database error: %s" % e)
                conn.close()
                return f"@{user} Database error: {e}"
            except Exception as e:
                print("Database error: %s" % e)
                conn.close()
                return f"@{user} Database error: {e}"

        if len(perms) < 1:
            if "-s" in params:
                perms = "-s"  # subonly
            elif "-m" in params:
                perms = "-m"  # modonly
            elif "-kb" in params:
                perms = "-kb"  # Bubba Kit and Boradcaster Only
            else:
                perms = "-e"  # for Everyone

        async with sqlite3.connect(database.pwd + "\\data\\commands.db") as conn:
            sql = f"REPLACE INTO commands('ComName', 'ComPerm', 'ComOutput') " \
                f"VALUES ('{comadd}', '{perms}', '{output}')"
            try:
                conn.execute(sql)
                conn.commit()
                conn.close()
                return f"@{user} Command Added {comadd}"
            except sqlite3.Error as e:
                print("Database error: %s" % e)
                conn.close()
                return f"@{user} Database error: {e}"
            except Exception as e:
                print("Exception in _query: %s" % e)
                conn.close()
                return f"@{user} Exception in _query: {e}"

    if not 'cmdadd' in command and not 'cmddel' in command:
        conn = sqlite3.connect(database.pwd + "\\data\\commands.db")
        try:
            cur = conn.cursor()
            cur.execute("SELECT * FROM commands")
            rows = cur.fetchall()
            for row in rows:
                if command in row[0]:
                    com = row[0]
                    perms = row[1]
                    output = row[2]
                    test = False
                    if perms == "-e":
                        test = True
                    elif perms == "-s" and usermode > 3:
                        test = True
                    elif perms == "-m" and usermode > 4:
                        test = True
                    elif perms == "-kb" and usermode > 5:
                        test = True
                    if test and output in command:
                        return output
                    elif not test:
                        return "Permission Denied"
                    else:
                        return ""
        except sqlite3.Error as e:
            print("Database error: %s" % e)
            return f"@{user} Database error: {e}"
        except Exception as e:
            print("General error: %s" % e)
            return f"@{user} Database error: {e}"





