#!/usr/bin/python3

"""A tiny Python program to check that httpd is running.
Try running this program from the command line like this:
  python3 check_webserver.py
"""

import subprocess

file_instanceIP = open("instanceID.txt", "r")

global instanceIP

instanceIP = file_instanceIP.read()

def checkhttpd():
  try:
    cmd = 'ps -A | grep httpd' 
   
    subprocess.call(cmd, check=True, shell=True)
    print("Web Server IS running")
   
  except subprocess.CalledProcessError:
    print("Web Server IS NOT running")
    startCmd = 'sudo systemctl start httpd'
    subprocess.call(startCmd, check=True, shell=True)
    
# Define a main() function.
def main():
    checkhttpd()
      
# This is the standard boilerplate that calls the main() function.
if __name__ == '__main__':
  main()

