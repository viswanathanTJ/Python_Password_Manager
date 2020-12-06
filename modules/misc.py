import secrets as s
import hashlib as h

# MISC FUNCTION
def randomStr(x):
    dictionary = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890-_+=@[](),./#~!£$%^&*:;"
    string = ""
    for _ in range(x):
        string += s.choice(dictionary)
    return string

def gen_sha3512_hash(x): 
    obj = h.sha3_512()
    obj.update(x.encode())
    return str(obj.hexdigest())

def genShadow():
    x = randomStr(8092)
    shadow = gen_sha3512_hash(x)
    return shadow

global R
global C
global Y
global G
global W

W = '\033[37m'
R = '\033[31m'
C = '\033[36m'
Y = '\033[33m'
G = '\033[32m'

def helper():
    print(Y+"[*] To get help add '-h' after main.py")
    print("[*] To Sign Up add '-a' after main.py")
    print("[*] To LogIn just run main.py")
    print("[*] To directly LogIn with master account run main.py '--m'")
    print("[*] Press [Ctrl+C] anytime to exit"+W)