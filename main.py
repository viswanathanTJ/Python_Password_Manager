from modules.router import helper, logIn, signUp, masterUser, masterUserLogin
import glob
import sys
import os

os.system('color')
os.chdir(sys.path[0])


if os.path.exists('Databases'):
    os.chdir('Databases')
else:
    os.mkdir('Databases')
    os.chdir('Databases')

if __name__ == "__main__":
    try:
        if len(sys.argv) > 1:
            if sys.argv[1] == '-a':
                signUp()
                sys.exit()
            if sys.argv[1] == '--m':
                if glob.glob('master.db'):
                    masterUserLogin()
                else:
                    masterUser()
                sys.exit()
            if sys.argv[1] == '-h':
                helper()
                sys.exit()
        if glob.glob('*.db') and not glob.glob('master.db'):
            logIn()
        else:
            helper()
            signUp()
            sys.exit()
    except KeyboardInterrupt:
        print("\nGood Bye"+'\033[0m')
