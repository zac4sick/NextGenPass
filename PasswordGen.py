import string #importing libraries and os
try:import posix as os
except:import os
import sys
from random import random,choice
from termcolor import cprint,colored
from time import sleep
import time
import base64
import hashlib
from Crypto import Random
from Crypto.Cipher import AES
import pyperclip #for copyboard function
import msvcrt #Functioning for windows services
import shutil
import zipfile
import json


password_placeholder='*'
max_index=51

def clear():
   if os.name=='posix':_=os.system('clear')
   else:_=os.system('cls')

def generate_random_password(maxr=40):
    symbols=['!','@','#','$','%','&','_','+','?','/','*',"'",'"']
    source = string.ascii_uppercase + string.ascii_lowercase + string.digits+choice(symbols)  
    return ''.join(choice(f"{source},{choice(symbols)}{choice(symbols)}") for x in range(1,maxr))  #joining source and randomly selected symbols 

def initialize(path): #path intialization
    with open(path,"r") as rnf:
        exec(rnf.read())
        clear()

def password_input(prompt=''): #Taking the password input 
    p_s = ''
    proxy_string = [' '] * max_index
    while True:
        sys.stdout.write('\x0D' + prompt + ''.join(proxy_string)) 
        c = msvcrt.getch()
        if c == b'\r':break
        elif c == b'\x08':
            p_s = p_s[:-1]
            proxy_string[len(p_s)] = " "
        else:
            proxy_string[len(p_s)] = password_placeholder
            p_s += c.decode()

    sys.stdout.write('\n')
    return p_s

def compress(files,archive,password): #archiving password
    with zipfile.ZipFile(archive, "w") as zf:
        for file in files:
            zf.write(file)

        zf.setpassword(password)

    with zipfile.ZipFile(archive, "r") as zf:
        crc_test = zf.testzip()
        if crc_test is not None:
            print(f"Bad CRC or file headers: {crc_test}")

        info = zf.infolist() 

        file = info[0]
        with zf.open(file) as f:
            f.read().decode()


        #zf.extract(file, "/tmp", pwd=password)

if __name__=="__main__":
    clear()
    print('Password: ',password_input("Enter password: "))
    print('Generated Random password (70-bit):',generate_random_password(70))
    print('Generated Random password (Default):',generate_random_password())
    
