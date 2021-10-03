import mysql.connector
import datetime

def connect():
    mydb = mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = "root",
        database = "TEST0610"
    )
    return mydb

def insert_to_time(player, passTime, playTime):
    mydb = connect()
    mycursor = mydb.cursor()
    sql = "INSERT INTO gamehistory_time (name, passTime, playTime) VALUES (%s, %s, %s)"
    val = (player, passTime, playTime)
    mycursor.execute(sql, val)
    mydb.commit()
    print(mycursor.rowcount, "record inserted.")

def insert_to_score(player, playTime, score):
    mydb = connect()
    mycursor = mydb.cursor()
    sql = "INSERT INTO gamehistory_ar (name, score, playTime) VALUES (%s, %s, %s, %s)"
    val = (player, score, playTime)
    mycursor.execute(sql, val)
    mydb.commit()
    print(mycursor.rowcount, "record inserted.")


def sort_final_time():
    mydb = connect()
    mycursor = mydb.cursor()
    mycursor.execute("SELECT name, passTime, playTime FROM gamehistory_time order by passTime limit 3")
    myresult = mycursor.fetchall()
    for x in myresult:
        for i in x:
            print(i)

def sort_final_ar():
    mydb = connect()
    mycursor = mydb.cursor()
    mycursor.execute("SELECT name, score, playTime FROM gamehistory_ar order by passTime limit 3")
    myresult = mycursor.fetchall()
    for x in myresult:
        for i in x:
            print(i)

def getCurrentTime():
    x = datetime.datetime.now()
    y =  str(x)
    y = y[:y.find(".")]
    return y
