import re
import os
import json
import requests
import argparse

parser = argparse.ArgumentParser()

parser.add_argument('command', help = 'command')

parser.add_argument('-u','--username', help = 'Username associated with Pastebin Account')
parser.add_argument('-p','--password', help = 'Password of Pastebin Account')
parser.add_argument('-d','--devkey', help = 'Developer Key or API Key')
parser.add_argument('-f','--force', help = 'Forcefully Configure', action = 'store_false')
parser.add_argument('-m','--message', help = 'Message to Paste')
parser.add_argument('-e','--expires', help = 'Message expires after', default = "10M")
parser.add_argument('--type', help = 'Exposure of the Paste')
parser.add_argument('-t','--title', help = 'Title of the Paste', default = "Untitled")
parser.add_argument('-k','--key', help = 'Key of the Paste')

args = parser.parse_args()

endpoint = "https://pastebin.com/api"

# Configuration
if args.command == 'configure':
    if os.path.exists("credentials.json") and args.force:
        print('Configuration Exists. To Overwrite, Use "-f" or "--force" flag.')
    else:
        data = {
            "api_dev_key" : args.devkey,
            "api_user_name" : args.username,
            "api_user_password" : args.password
        }

        response = requests.post(f"{endpoint}/api_login.php", data = data)
        if response.status_code == 401:
            print('Provide Valid Credentials.')
        elif response.status_code == 200:
            data.update({"api_user_key": response.text})
            with open('credentials.json', 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4)

            print("Configuration Success! You can start using other commands.")
        
# Create Paste
if args.command == 'create':
    if os.path.exists("credentials.json"):
        with open('credentials.json', 'r') as f:
            data = json.load(f)

        response = requests.post(f"{endpoint}/api_post.php", data = {
            "api_dev_key" : data['api_dev_key'],
            "api_user_key" : data['api_user_key'],
            "api_paste_code" : args.message,
            "api_paste_name" : args.title,
            "api_option" : "paste",
            "api_paste_private" : "0" if args.type == 'public' else "2",
            "api_paste_expire_date" : args.expires
        })

        if response.status_code == 200:
            print(response.text)
        else:
            print(f"Error occurred while Creating a new paste. Status code: {response.status_code}")
    else:
        print('Missing Credentials. Run "python3 pasteman.py configure"')

# Retrieve Private Pastes
if args.command == "list":
    if os.path.exists("credentials.json"):
        with open('credentials.json', 'r') as f:
            data = json.load(f)

        response = requests.post(f"{endpoint}/api_post.php", data = {
            "api_dev_key" : data['api_dev_key'],
            "api_user_key" : data['api_user_key'],
            "api_option" : "list"
        })

        def remove_tags(string):
            return string.replace('<paste_key>','').replace('</paste_key>','').replace('<paste_title>','').replace('</paste_title>','')

        paste_keys = re.findall(r'<paste_key>.*</paste_key>', response.text)
        paste_titles = re.findall(r'<paste_title>.*</paste_title>', response.text)

        keys_iterator = map(remove_tags, paste_keys)
        titles_iterator = map(remove_tags, paste_titles)

        print(f"Keys : {list(keys_iterator)}")
        print(f"Titles : {list(titles_iterator)}")
    
    else:
        print('Missing Credentials. Run "python3 pasteman.py configure"')

# Retrieve Raw Content
if args.command == 'retrieve':
    if os.path.exists("credentials.json") and args.key != None:
        with open('credentials.json', 'r') as f:
            data = json.load(f)

        response = requests.post(f"{endpoint}/api_raw.php", data = {
            "api_dev_key" : data['api_dev_key'],
            "api_user_key" : data['api_user_key'],
            "api_option" : "show_paste",
            "api_paste_key" : args.key
        })

        print(response.text)

# Delete a Private Paste
if args.command == 'delete':
    if os.path.exists("credentials.json") and args.key != None:
        with open('credentials.json', 'r') as f:
            data = json.load(f)

        response = requests.post(f"{endpoint}/api_post.php", data = {
            "api_dev_key" : data['api_dev_key'],
            "api_user_key" : data['api_user_key'],
            "api_option" : "delete",
            "api_paste_key" : args.key
        })

        print(response.text)