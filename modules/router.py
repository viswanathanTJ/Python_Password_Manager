from modules.db import *
from modules.misc import *
from modules.functions import homepage
from os import path

# SIGNUP
def signUp():
    print(R + '*'*32)
    print('*' + W + ' Sign Up with new Credentials ' + R + '*')
    print('*'*32)
    while True:
        name = input(G+'[*] Enter Username:'+W)
        if name == '':
            print(R+'Username cannot leave blank')
            continue
        break
    while True:
        password = input(G+'[*] Enter Password:'+W)
        if len(password) < 4:
            print(Y+'Password must be atleast 4 characters')
            continue
        break
    if path.exists(name+'.db'):
        print(R+'[!!] User already exists')
    else:
        createDBTableUser(name)
        userHash = gen_sha3512_hash(name)
        shadow = genShadow()
        passShadow = password + shadow
        passHash = gen_sha3512_hash(passShadow)
        newUserAdder(userHash, passHash, shadow)
        print(C+'[+] New User Credentials Added :)\n')
        print(G+'[+] Run program again to LogIn')

# LOGIN
def logIn():
    print(Y+"[*] To Sign Up add '-a' after main.py")
    print(R+"[*] Press [Ctrl+C] to exit")
    print(C+'-'*28)
    print('| '+W+'Sign In with Credentials'+C+' |')
    print('-'*28)
    n = 3
    while n > 0:
        while True:
            username = input(G+'[+] Enter Username:'+W)
            if username == '':
                print(R+'Username cannot leave blank')
                continue
            break
        while True:
            password = input(G+'[*] Enter Password:'+W)
            if len(password) < 4:
                print(Y+'Password must be atleast 4 characters')
                continue
            break
        if username and password != '':
            if path.exists(username+'.db'):
                DBConnector(username)
                shadowDB = getUserShadowDB()
                passDB = getUserPassDB()
                passShadow = password + shadowDB
                passHash = gen_sha3512_hash(passShadow)
                if passHash == passDB:
                    homepage(username)
                else:
                    print(R+'-'*22)
                    print('| '+W+'[-] Wrong Password'+R+' |')
                    print(R+'-'*22)
                    n = n-1
            else:
                print(R+'-'*21)
                print('| '+W+'[-] DB not exists'+R+' |')
                print('-'*21)
                n = n-1
        else:
            print(R+'-'*41)
            print('| '+W+'[!!] Enter both username and password'+R+' |')
            print('-'*41)
    print("[-] Too many attempts, Try again later")

# Master User
def masterUser():
    print(Y+'[#] SignUp first run')
    while True:
        password = input(G+'[+] Enter New Master Password:'+W)
        if len(password) < 4:
            print(Y+'Password must be atleast 4 characters')
            password = input(G+'[+] Enter New Master Password:'+W)
            continue
        break
    createDBTableUser('master')
    userHash = gen_sha3512_hash('master')
    shadow = genShadow()
    passShadow = password + shadow
    passHash = gen_sha3512_hash(passShadow)
    newUserAdder(userHash, passHash, shadow)
    print(C+'[+] Master Password Added :)\n')
    print(G+'[+] Run program with --m to directly logIn with master mode')


def masterUserLogin():
    print(R+"[*] Press [Ctrl+C] to exit")
    print(C+'-'*28)
    print('| '+W+'Sign In with Credentials'+C+' |')
    print('-'*28)
    n = 3
    while n > 0:
        password = input(G+'[+] Enter Master Password:'+W)
        if password != '':
            DBConnector('master')
            shadowDB = getUserShadowDB()
            passDB = getUserPassDB()
            passShadow = password + shadowDB
            passHash = gen_sha3512_hash(passShadow)
            if passHash == passDB:
                homepage('master')
            else:
                print(R+'-'*22)
                print('| '+W+'[-] Wrong Password'+R+' |')
                print('-'*22)
                n = n-1
    print(R+"[-] Too many attempts, Try again later")
