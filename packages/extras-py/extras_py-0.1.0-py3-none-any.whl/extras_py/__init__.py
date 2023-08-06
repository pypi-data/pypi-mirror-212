__version__ = '0.1.0'

class extras-py:
  def __init__():
    import time,random
    from os import system,name
    import sys
    import os
    from time import sleep
    from colorama import Fore as F
    from colorama import Style as S
    from os import system as syst
    from replit import db
    bright = S.BRIGHT
    normal = S.NORMAL
    blue = F.BLUE
    white = F.WHITE
    green = F.LIGHTGREEN_EX
    red = F.RED
    yellow = F.LIGHTYELLOW_EX
    purple = F.LIGHTMAGENTA_EX
    light_blue = F.LIGHTBLUE_EX
    
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
    
    def wait(time):
      time.sleep(time)