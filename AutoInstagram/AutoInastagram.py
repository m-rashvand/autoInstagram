# autoInstagram is an script for automating instagram tasks
# developed by @mRashvand
import sys
import pathlib
import re
from time import sleep
from typing import Dict
from download import Download
from login import Login

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.remote.webdriver import WebDriver


class AutoInastagram():

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
                         r'(?P<COMMAND>--download|-d)\s?(?P<D_Count>\d+)?', # download the post media from url or a user's  post
                         r'(?P<COMMAND>--follow|-f)\s?', # follow given user(s)
                         r'(?:--output|-o)\s(?P<OUT>.+)\s']
                         
      operand_pattern = [r'@(?!.*\.$)[^\W](?P<INSTA_USER>[\w.]{0,29})', # get single instagram username
                         r'(?:(?:http|https):\/\/)(?:www.)?(?:instagram.com|instagr.am|instagr.com)\/((?P<POSTFLAG>p)\/)?(?P<ID>[\w.]+)', # get instagram username or post id
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
      print(result)
      sleep(5)
      return result
      
      
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
      # TODO ADD MORE COMMANDS 

      if not 'COMMAND' in args:
         print('No Cammand provided')
         return

      if args['COMMAND'] == '--download' or args['COMMAND'] == '-d':
         d = Download(args['ID'], args['OUT'])
         d.download()
              
      else:
         pass

   def start(self):
      parsed_args = self.parse(' '.join(self.args[:-1]), self.args[-1])

      l = Login(parsed_args['USER'], parsed_args['PASS'])
      is_authenticated, cookies, user_agent = l.login()
      if is_authenticated:
         self.cookies = cookies
         self.user_agent = user_agent
         self.arg_handler(parsed_args)

# testing 
ai = AutoInastagram(sys.argv[1:])
ai.start()
