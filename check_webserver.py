#!/usr/bin/python3

"""A tiny Python program to check that httpd is running.
Try running this program from the command line like this:
  python3 check_webserver.py
"""

import subprocess

#Creating colour class in order to change text colour
class bcolors:
    
    OKGREEN = '\033[92m' #Green
    FAIL = '\033[91m' #Red
    ENDC = '\033[0m' #white to revert back to white colour

file_instanceIP = open("instanceID.txt", "r")

global instanceIP

instanceIP = file_instanceIP.read()

def checkhttpd():
  try:
    cmd = 'ps -A | grep httpd' 
   
    subprocess.call(cmd, check=True, shell=True)
    print(bcolors.OKGREEN + "Web Server IS running" + bcolors.ENDC)
   
  except subprocess.CalledProcessError:
    print(bcolors.FAIL + "Web Server IS NOT running, attempting to start" + bcolors.ENDC)
    startCmd = 'sudo systemctl start httpd'
    subprocess.call(startCmd, check=True, shell=True)
    
# Define a main() function.
def main():
    checkhttpd()
      
# This is the standard boilerplate that calls the main() function.
if __name__ == '__main__':
  main()

