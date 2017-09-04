import sqlite3
import time


def dohoteltasks(taskname, parameter):
    _connect = sqlite3.connect('cronhoteldb.db')
    cur = _connect.cursor()
    if taskname == 'clean':
        cur.execute("""SELECT RoomNumber FROM Rooms
                     WHERE RoomNumber NOT IN (SELECT RoomNumber FROM Residents) ORDER BY RoomNumber ASC
        """)
        res = ""
        for row in cur.fetchall():
            res += str(row[0])
            res += ', '
        res = res[:len(res) - 2]
        print 'Rooms {} were cleaned at {}'.format(res, time.time())
    else:
        cur.execute("SELECT * FROM Residents WHERE RoomNumber = ?", [parameter])
        res = cur.fetchone()
        if taskname == 'breakfast':
            print '{} {} in room {} has been served breakfast at {}'.format(res[1], res[2], parameter, time.time())
        elif taskname == 'wakeup':
            print '{} {} in room {} received a wakeup call at {}'.format(res[1], res[2], parameter, time.time())