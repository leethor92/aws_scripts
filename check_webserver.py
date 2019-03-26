#!/usr/bin/python3

"""A tiny Python program to check that httpd is running.
Try running this program from the command line like this:
  python3 check_webserver.py
"""

import subprocess

def checkhttpd():
  cmd = 'ps -A | grep httpd'
   
  (status, output) = subprocess.getstatusoutput(cmd)
  if status == 0:
    print("Web Server IS running")
  else:
    print("Web Server IS NOT running")
    print("Attempting to boot apache now")
    cmd = 'sudo systemctl start httpd'
    subprocess.run(cmd, shell=True)
    if status == 0:
      print("Web server is not running")
    else:
      print("Web server is running")

# Define a main() function.
def main():
    checkhttpd()

# This is the standard boilerplate that calls the main() function.
if __name__ == '__main__':
  main()

