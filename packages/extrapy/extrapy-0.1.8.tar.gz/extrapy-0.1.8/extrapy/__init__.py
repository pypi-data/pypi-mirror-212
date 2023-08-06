__version__ = '0.1.8'

import time,random
from os import system,name
import sys
import os
from time import sleep
import time
from os import system as syst
from replit import db
    
def clear():
     
        # for windows
    if name == 'nt':
        _ = system('cls')
     
        # for mac and linux(here, os.name is 'posix')
    else:
        _ = system('clear')
    
def br(times):
  for i in range(times):
    print()
    
def write(words):
  for i in (F.WHITE + words):
    sys.stdout.write(i)
    sys.stdout.flush()
    sleep(.03)
    
def wait(t):
  time.sleep(t)