#!/usr/local/bin/python3 -tt

import sys
import os
from _collections import deque
import requests
from bs4 import BeautifulSoup

def GetPageByElements(soupy):
    # Elements of interest are: p, head, a, ul, ol, li
    tag_dict = {}
    for tag in soupy.find_all(['a', 'p', 'header', 'title', 'ul', 'ol', 'li', 'h1', 'h2', 'h3', 'h4', 'h5']):
        tag_dict[tag.sourceline] = tag.text
    text = ''
    for k, v in sorted(tag_dict.items()):
        if v == '\n' or v == '':
            continue
        elif str(v) in text:
            continue
        elif str(v).endswith('\n'):
            text += v
        else:
            text += v + '\n'
    print('Dictionary len is: ', len(tag_dict))
    print('Length of text is: ', len(text))
    return text

# write your code here
args = sys.argv[1:]
if len(args) > 1:
    print('Too many arguments passed!')
    sys.exit()
url_save_location = os.path.join(os.getcwd(), args[0])

if not os.path.exists(url_save_location):
    os.makedirs(url_save_location)

os.chdir(url_save_location)
allowed_domains = ['.com', '.org', '.net']
prev_pages = deque()
current_url = ''
last_url = ''

while True:
    if last_url != '':
        prev_pages.append(last_url)

    user_url = input()
    last_period_index = user_url.rfind('.')

    if last_period_index == -1:
        if user_url in os.listdir(os.getcwd()):
            last_url = current_url
            current_url = user_url
            with open(user_url, 'r') as f:
                print(f.read())
            continue
        elif user_url == 'exit':
            os.chdir('..')
            break
        elif user_url == 'back':
            if len(prev_pages) == 0:
                continue
            else:
                with open(prev_pages.pop(), 'r') as f:
                    print(f.read())
                last_url = ''
                continue
        else:
            last_url = ''
            print('Error:  Incorrect URL')
            continue

    if user_url.startswith('https'):
        top_level_domain = user_url[last_period_index:last_period_index + 4]
        file_name = user_url[8:last_period_index]
    else:
        top_level_domain = user_url[last_period_index:last_period_index + 4]
        file_name = user_url[:last_period_index]

    # check to see if user had full URL
    if not user_url.startswith('http'):
        user_url = 'https://' + user_url

    # Get webpage
    req = requests.get(user_url)
    print('User URL: ', user_url)
    print('Request status: ', req.status_code)
    print('Request Length: ', len(req.content))
    if not req:
        last_url = ''
        print('Error:  Incorrect URL')
        continue

    # Print webpage, write it to cache and set last & current URL
    soup = BeautifulSoup(req.content, 'html.parser')
    print('Soup len equals: ', len(soup))
    page = GetPageByElements(soup)
    #print(page)
    last_url = current_url
    current_url = file_name
    with open(file_name, 'w+') as f:
        f.write(page)

