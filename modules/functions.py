import os
from modules.db import *
from modules.enc import *
from modules.router import *
from modules.misc import *
import shutil, sys

# HomePage
def homepage(name):
    while True:
        print(C+f'\n[*] Welcome {name} [*]')
        print(W+'''
1.Add Password
2.View Password
3.Update Stored Password
4.Delete Password
5.Advanced Options
99.Help
''')
        prompt = input(G+'[+] Enter option (1 - 5):'+W)    
        while True:
            if prompt == '1':
                domain = input(G+"Enter domain/url:"+W)
                username = input(G+"Enter username:"+W)
                password = input(G+"Enter password:"+W)
                addPassword(domain, username, password)
                print(C+'*'*18)
                print('* '+W+'Password Added'+C+' *')
                print('*'*18)
                if input(Y+'[+] Do you want to add another[y]:'+W) == 'y':
                    continue
                else:
                    break
            elif prompt == '2':
                cond = viewer()
                if cond == False:
                    print(R+'-'*36)
                    print('| '+W+'[-] Error no records found in DB'+R+' |')
                    print('| '+W+'[+]        Try adding one       '+R+' |')
                    print('-'*36)
                    break
                print(Y+'*'*34)
                print('* '+W+'      Stored Passwords        '+Y+' *')
                print('*'*34)
                viewDBPassword()
                break
            elif prompt == '3':
                cond = viewer()
                if cond == False:
                    print(R+'-'*36)
                    print('| '+W+'[-] Error no records found in DB'+R+' |')
                    print('| '+W+'[+]        Try adding one       '+R+' |')
                    print('-'*36)
                    break
                user_input = input(G+"[+] Enter ID/Domain to update:"+W)
                if updater(user_input) == False:
                    print(R+'-'*48)
                    print('| '+W+'[-] Error no records found on that ID/Domain '+R+' |')
                    print('| '+W+'[+]       Try viewing stored password        '+R+' |')
                    print('-'*48)
                    break
                print(G+'*'*24)
                print('* '+W+'Updated Successfully'+G+' *')
                print('*'*24)
                break
            elif prompt == '4':
                cond = viewer()
                if cond == False:
                    print(R+'-'*36)
                    print('| '+W+'[-] Error no records found in DB'+R+' |')
                    print('| '+W+'[+]        Try adding one       '+R+' |')
                    print('-'*36)
                    break
                user_input = input(G+"Enter ID to delete:")
                cond = deleter(user_input)
                if cond == False:
                    print('-'*48)
                    print('| '+W+'[-] Error no records found on that ID '+R+' |')
                    print('| '+W+'[+]     Try viewing stored password   '+R+' |')
                    print('-'*48)
                    break
                print(G+'*'*33)
                print('* '+W+'1 Record Deleted Successfully'+G+' *')
                print('*'*33)
                if input(Y+'Do you want to delete another[y]:'+W) == 'y':
                    continue
                else:
                    break
            elif prompt == '5':
                advancedOptions(name)
                break
            elif prompt == '99':
                helper()
                break
            else:
                print(R+'[-] Invalid Input'+W)
                break
            
# Advanced Options
def advancedOptions(name):
    print(C+'-'*20)
    print('| '+W+'Advanced Options'+C+' |')
    print('-'*20)
    print(W+'''
1.Backup db
2.Restore db
3.Reset Master Password
88.Delete Database
99.Show DB[Debugging Only]
''')
    prompt = input(G+'[+] Enter option:'+W) 
    if prompt == '1':
        sourceFile = name + '.db'
        shutil.copy(sourceFile,sourceFile+'.bkp')
        print(G+'-'*25)
        print('| '+W+'[+] Backup Successfull'+G+' |')
        print('-'*25)
    elif prompt == '2':
        try:
            if input(Y+'[!!] Warning if new passwords not backed up will not restored[y]:'+W) == 'y':
                sourceFile = name + '.db'
                shutil.copy(sourceFile+'.bkp',sourceFile)
                print(G+'-'*26)
                print('| '+W+'[+] Restore Successfull'+G+' |')
                print('-'*26)
        except:
            print(R+'-'*27)
            print('| '+W+'[-] Backup file not found'+R+' |')
            print('-'*27)
    elif prompt == '3':
        cond = resetLogin()
        if cond == True:
            while True:
                pass1 = input(G+"[+] Enter new master Password:"+W)
                if len(pass1) < 4:
                    print(Y+"[-] Password should be greater than 4 characters")
                    continue
                break
            pass2 = input(G+"[+] Enter new master Password again:"+W)
            if pass1 == pass2:
                changePassword(pass1)
            else:
                print(R+'-'*41)
                print('| '+W+'[-]Passwords does not match Try again'+R+' |')
                print('-'*41)
        else:
            print(R+'-'*22)
            print('| '+W+'[-] Wrong Password'+R+' |')
            print('-'*22)
    elif prompt == '88':
        if input(R+'[!!] Warning all datas inside will be deleted forever[y]:'+W) == 'y':
            dbCloser()
            os.remove(name+'.db')
            print(G+'-'*33)
            print('| '+W+'Database Deleted Successfully'+G+' |')
            print('-'*33)
            sys.exit()
        else:
            print(R+'[-] Wrong Input. Nothing deleted'+W)
    elif prompt == '99':
        printDB()
    else:
        print(R+'[-] Invalid Input'+W)

# RESET 
def resetLogin():
    password = input(Y+"Enter old password:"+W)
    shadowDB = getUserShadowDB()
    passDB = getUserPassDB()
    passShadow = password + shadowDB
    passHash = gen_sha3512_hash(passShadow)
    if passHash == passDB:
        return True
    else:
        print(R+'[-] Wrong Password')
  
# Change Password      
def changePassword(password):
    shadow = genShadow()
    passShadow = password + shadow
    passHash = gen_sha3512_hash(passShadow)
    updatePass(passHash, shadow)
    shadow = ""
    passShadow = ""
    passHash = ""
    print(G+'-'*53)
    print('| '+W+'      [:)] Password has been Updated in db       '+G+' |')
    print('| '+W+'[*]Start program again to LogIn with new Password'+G+' |')
    print('-'*53)
    sys.exit()

# ADD PASSWROD
def addPassword(domain, username, password):
    key = getUserPassDB()
    username_enc = encryptor(username, key)
    password_enc = encryptor(password, key)
    addNewPassword(domain, username_enc, password_enc)
   
# Updater 
def updater(ID):
    if printRow(ID) == True:
        newPass = input(G+"Enter new Password:"+W)
        key = getUserPassDB()
        pass_enc = encryptor(newPass, key)
        updateManagerPass(pass_enc, ID)
        print(G+"[+] Password Updated Successfully")
    else:
        return False
