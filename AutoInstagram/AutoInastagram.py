# autoInstagram is an script for automating instagram tasks
# developed by @mRashvand
import time
import sys
import pathlib
import getpass
import re
import requests
import json
from datetime import datetime
from typing import Dict
import random as rand
# import threading
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.remote.webdriver import WebDriver


class AutoInastagram():

   user_agents = ['Mozilla/5.0 (X11; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0',
                  'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:78.0) Gecko/20100101 Firefox/78.0',
                  'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36',
                  'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36']
                  
   BASE_URL = 'https://www.instagram.com/accounts/login/'


   def __init__(self, args):
      self.args = args
      self.driver: WebDriver
      self.cookies: any
      self.user_agent: str


   def parse(self, options: str, operand: str) -> Dict[str, str]:
      '''
         Get command line arguments and seperate them using regex.
         Return value:
            A dictionary of {Option: Option-arguments} and operand
      '''
      options_pattern = [r'(?:--pass|-p)\s(?P<PASS>.+?)(?= -)',  # password used in autification
                         r'(?:--user|-u)\s(?P<USER>[\w.]{0,29})\s', # username used in autification 
                         r'(?:--list)\s(?P<LIST>.+\.txt)', # get input file path that contains instagram urls
                         r'(?P<COMMAND>--download|-d)\s(?P<D_Count>\d+)?', # download the post media from url or a user's  post
                         r'(?P<COMMAND>--follow|-f)\s', # follow given user(s)
                         r'(?:--output|-o)\s(?P<OUT>.+)\s']
                         
      operand_pattern = [r'(?!.*\.$)[^\W](?P<INSTA_USER>[\w.]{0,29})', # get single instagram username
                         r'(?:(?:http|https):\/\/)(?:www.)?(?:instagram.com|instagr.am|instagr.com)\/(?P<POSTFLAG>p\/)?(?P<ID>[\w.]+)', # get instagram username or post id
                         r'(?P<FILE>.+\.txt)'] 
      operand_pattern = '^' + '|'.join(operand_pattern) + '$'

      result: Dict[str, str] = {}
      # match all options and option-arguments and add them to dict
      options_match = list(re.search(regex, options) for regex in options_pattern)
      result = {key: val for opm in options_match
                      if opm is not None
                        for key, val in opm.groupdict().items()
                        if val is not None}
      
      # detect the only operand and add it to dict
      operand_match = re.search(operand_pattern, operand)
      for key, val in operand_match.groupdict().items():
         if val is not None:
            result[key] = val
      
      return result
      
   def login(self, username: str, password: str):
      time = int(datetime.now().timestamp())
      response = requests.get(self.BASE_URL)
      csrf = response.cookies['csrftoken']

      payload = {
         'username': username,
         'enc_password': f'#PWD_INSTAGRAM_BROWSER:0:{time}:' + password,
         'queryParams': {},
         'optIntoOneTap': 'false'
      }
      
      header = {
         'User-Agent': self.user_agents[rand.randint(0,3)],
         'X-Requested-With': 'XMLHttpRequest',
         'Referer': self.BASE_URL,
         'x-csrftoken': csrf
      }

      login_response = requests.post(
         self.BASE_URL + 'ajax/', data=payload, headers=header)
      json_data = json.loads(login_response.text)

      print(login_response.text)
      if json_data["authenticated"]:
         print("successful login.")
         
         self.cookies = login_response.cookies.get_dict()
         return True
      else:
         print("login failed.")

         if not json_data['user']:
            print(f"User '{username}', is not found")
         elif not json_data["authenticated"]:
            print(f'Wrong password.')
         else:
            print(json_data['status'])
         return False
      

   def selenium(self):
      print("Starting the Browser ...")
      self.driver = webdriver.Chrome(
          executable_path=r''+str(pathlib.Path().absolute())+'\chromedriver.exe')

      print("Loading the Site ...")
      self.driver.get(self.BASE_URL)
      # convet and add cookies to selenium driver
      for cookie in self.cookies:
         self.driver.add_cookie({"name": cookie, "value": self.cookies[cookie]})

      self.driver.get(self.BASE_URL)
      

   def arg_handler(self, args):
      succesful = self.login(args['USER'], args['PASS'])

      if not succesful:
         return
      
      # TODO ADD COMMANDS 

      if args['COMMAND'] == '--download' or args['COMMAND'] == '-d':
         pass
              
      else:
         pass

   def start(self):
      parsed_args = self.parse(' '.join(self.args[:-1]), self.args[-1])
      print(parsed_args)
      self.arg_handler(parsed_args)
   {'PASS': '55sdl 5', 'USER': 'sdasd', 'INSTAUSER': 'ijsjidvff'}

# testing 
ai = AutoInastagram(sys.argv[1:])
ai.start()
