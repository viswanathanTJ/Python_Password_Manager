from modules.dec import decryptor
import sqlite3
import os

sql_inserter = 'INSERT INTO MANAGER (DOMAIN,USERNAME, PASSWORD) VALUES (?,?,?)'
C = '\033[36m'
W = '\033[37m'
G = '\033[32m'

# SIGNUP
def createDBTableUser(username):
    global user
    user = sqlite3.connect(username+'.db')
    user.execute('''CREATE TABLE IF NOT EXISTS USER
        (USERNAME TEXT NOT NULL,
        PASSWORD TEXT NOT NULL,
        SHADOW TEXT NOT NULL);'''
        )
    user.execute('''CREATE TABLE IF NOT EXISTS MANAGER
        (ID INTEGER PRIMARY KEY AUTOINCREMENT,
        DOMAIN TEXT NOT NULL,
        USERNAME TEXT NOT NULL,
        PASSWORD TEXT NOT NULL);'''    
        )
    user.commit()
    

def newUserAdder(username, password, shadow):
    cursor = user.cursor()
    sql_user_adder = 'INSERT INTO USER (USERNAME,PASSWORD,SHADOW) VALUES (?,?,?)'
    cursor.execute(sql_user_adder, (username, password,shadow,))
    user.commit()
    
# LOGIN
def DBConnector(dbName):
    global user
    global userPassDB
    global userShadowDB
    user = sqlite3.connect(dbName+'.db')
    cursor = user.execute("SELECT PASSWORD, SHADOW from USER")
    for row in cursor:
        userPassDB = row[0]
        userShadowDB = row[1]
    
def getUserPassDB():
    return userPassDB
def getUserShadowDB():
    return userShadowDB

def updatePass(password,shadow):
    user.execute("UPDATE USER SET PASSWORD=?, SHADOW=?", (password, shadow))
    user.commit()
    
# FUNCTIONS
# ADD
def addNewPassword(domain, username, password):
    cursor = user.cursor()
    cursor.execute(sql_inserter, (domain, username, password,))
    user.commit()

# VIEW
def viewer():
    view_cursor = user.execute("SELECT ID,DOMAIN,USERNAME,PASSWORD from MANAGER")
    data=view_cursor.fetchone()
    if data is None:
        return False
    return True

def viewDBPassword():
    view_cursor = user.execute("SELECT ID,DOMAIN,USERNAME,PASSWORD from MANAGER")
    key = getUserPassDB()
    for row in view_cursor:
        username = decryptor(row[2],key)
        password = decryptor(row[3],key)
        print(C+"[#]    ID    = "+W, row[0])
        print(C+"[#]  Domain  = "+W, row[1])
        print(C+"[#] Username = "+W, username)
        print(C+"[#] Password = "+W, password)
        print(G+'-'*34)

# UPDATE
def printRow(ID):
    cursor = user.execute("SELECT ID,DOMAIN,USERNAME,PASSWORD from MANAGER WHERE ID=? OR DOMAIN=?",(ID,ID,))
    data=cursor.fetchone()
    if data is None:
        return False
    key = getUserPassDB()
    username = decryptor(data[2],key)
    password = decryptor(data[3],key)
    print(C+"ID           = "+W, data[0])
    print(C+"Domain       = "+W, data[1])
    print(C+"Username     = "+W, username)
    print(C+"Old Password = "+W, password)
    return True

def updateManagerPass(newPass, ID):
    user.execute("UPDATE MANAGER SET PASSWORD=? WHERE ID=? OR DOMAIN=?",(newPass,ID,ID,))
    user.commit()
    
# DELETE
def deleter(ID):
    del_cursor = user.execute("SELECT PASSWORD from MANAGER WHERE ID=? OR DOMAIN=?",(ID,ID,))
    data = del_cursor.fetchone()
    if data is None:
        return False
    user.execute("DELETE FROM MANAGER WHERE DOMAIN=? OR ID=?", (ID,ID,))
    user.commit()
    return True

def dbCloser():
    user.close()
    
# SHOW DB Data
def printDB():
    print(G+"[+] User Credentials in DB [+]")
    cursor = user.execute("SELECT PASSWORD,SHADOW from USER")
    for row in cursor:
        print("Password = ", row[0])
        print("Shadow = ", row[1])
    print(G+"[+] Passwords stored in DB [+]")
    cursor = user.execute("SELECT ID,DOMAIN,USERNAME, PASSWORD from MANAGER")
    for row in cursor:
        print(C+"[#]    ID    = "+W, row[0])
        print(C+"[#]  Domain  = "+W, row[1])
        print(C+"[#] Username = "+W, row[2])
        print(C+"[#] Password = "+W, row[3])
        print(G+'-'*103)