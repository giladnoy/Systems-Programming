import os
import sqlite3
import atexit
import sys


if not (os.path.isfile('cronhoteldb.db')):
    _conn = sqlite3.connect('cronhoteldb.db')
else:
    exit()


# register a function to be called immediately when the interpreter terminates
def _close_db():
    _conn.commit()
    _conn.close()


atexit.register(_close_db)


def create_tables():
    _conn.executescript("""
        CREATE TABLE TaskTimes (
            TaskId INT PRIMARY KEY NOT NULL,
            DoEvery INT NOT NULL,
            NumTimes INT NOT NULL
        );

        CREATE TABLE Tasks (
            TaskId INT NOT NULL REFERENCES TaskTimes(TaskId),
            TaskName TEXT NOT NULL,
            Parameter INT
        );

        CREATE TABLE Rooms (
            RoomNumber INT PRIMARY KEY NOT NULL
        );

        CREATE TABLE Residents (
            RoomNumber INT NOT NULL REFERENCES Rooms(RoomNumber),
            FirstName TEXT NOT NULL,
            LastName TEXT NOT NULL
        );
    """)


def insert_TaskTime(TaskId, DoEvery, NumTimes):
    _conn.execute("""
        INSERT INTO TaskTimes (TaskId, DoEvery, NumTimes) VALUES (?, ?, ?)
    """, [TaskId, DoEvery, NumTimes])


def insert_Task(TaskId, TaskName, Parameter):
    _conn.execute("""
        INSERT INTO Tasks (TaskId, TaskName, Parameter) VALUES (?, ?, ?)
    """, [TaskId, TaskName, Parameter])


def insert_Room(RoomNumber):
    _conn.execute("""
        INSERT INTO Rooms (RoomNumber) VALUES (?)
    """, [RoomNumber])


def insert_Resident(RoomNumber, FirstName, LastName):
    _conn.execute("""
        INSERT INTO Residents (RoomNumber, FirstName, LastName) VALUES (?, ?, ?)
    """, [RoomNumber, FirstName, LastName])


def main(args):
    cur = _conn.cursor()
    create_tables()
    lines = []
    f = open(args[1])
    index = 0
    for line in f:
        lines.append(line.strip())
    for x in lines:
        y = x.split(',')
        if y[0] == 'room':
            insert_Room(y[1])
            if len(y) == 4:
                insert_Resident(y[1], y[2], y[3])

        elif y[0] == 'clean':
            insert_TaskTime(index, y[1], y[2])
            insert_Task(index, 'clean', 0)
            index += 1
        else:
            insert_TaskTime(index, y[1], y[3])
            insert_Task(index, y[0], y[2])
            index += 1

if __name__ == '__main__':
    main(sys.argv)