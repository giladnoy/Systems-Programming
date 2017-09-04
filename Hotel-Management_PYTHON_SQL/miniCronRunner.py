import sqlite3
import time
import hotelWorker
import sys
import atexit
import os

_conn = sqlite3.connect('cronhoteldb.db')
cur = _conn.cursor()

# register a function to be called immediately when the interpreter terminates
def _close_db():
    _conn.commit()
    _conn.close()

atexit.register(_close_db)

def main(args):
    cur = _conn.cursor()
    cur.execute("""
            SELECT * FROM TaskTimes INNER JOIN Tasks ON TaskTimes.TaskId = Tasks.TaskId
    """)
    taskTimer = {}
    taskCounter = 0
    for task in cur.fetchall():
        hotelWorker.dohoteltasks(task[4], task[5])
        taskTimer[task[0]] = time.time()
        cur.execute("""UPDATE TaskTimes
                    SET NumTimes = (NumTimes-1)
                    WHERE TaskTimes.TaskId =(?)
        """, [task[0]])
        cur.execute("SELECT * FROM TaskTimes")
        taskCounter += (task[2] -1)
    while (taskCounter > 0 and os.path.isfile('cronhoteldb.db')):
        cur.execute("""
                    SELECT * FROM TaskTimes INNER JOIN Tasks ON TaskTimes.TaskId = Tasks.TaskId
                    WHERE NumTimes > 0
        """)
        for row in cur.fetchall():
            if (time.time() - taskTimer[row[0]]) >= row[1] :
                hotelWorker.dohoteltasks(row[4], row[5])
                taskTimer[row[0]] = time.time()
                taskCounter -= 1
                cur.execute("""UPDATE TaskTimes
                            SET NumTimes = (NumTimes-1)
                            WHERE TaskTimes.TaskId =(?)
                """, [row[0]])
                cur.execute("""
                                    SELECT * FROM TaskTimes INNER JOIN Tasks ON TaskTimes.TaskId = Tasks.TaskId
                                    WHERE NumTimes > 0
                """)
if __name__ == '__main__':
    main(sys.argv)


