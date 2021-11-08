import requests
import json
from random import randint
from datetime import datetime


class Login():

   def __init__(self, username: str, password: str) -> None:
      self.username = username
      self.password = password
      self.cookies = None
      self.is_authenticated = False
      self.BASE_URL = 'https://www.instagram.com/accounts/login/'

      self.user_agents = [
          'Mozilla/5.0 (X11; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0',
          'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:78.0) Gecko/20100101 Firefox/78.0',
          'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36',
          'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36']

   def login(self):
      time = int(datetime.now().timestamp())
      response = requests.get(self.BASE_URL)
      csrf = response.cookies['csrftoken']
      ua = self.user_agents[randint(0, 3)]

      payload = {
         'username': self.username,
         'enc_password': f'#PWD_INSTAGRAM_BROWSER:0:{time}:' + self.password,
         'queryParams': {},
         'optIntoOneTap': 'false'
      }

      header = {
         'User-Agent': ua,
         'X-Requested-With': 'XMLHttpRequest',
         'Referer': self.BASE_URL,
         'x-csrftoken': csrf
      }

      login_response = requests.post(
          self.BASE_URL + 'ajax/', data=payload, headers=header)
      json_data = json.loads(login_response.text)

      if json_data["authenticated"]:
         print("successful login.")
         self.is_authenticated = True
         self.cookies = login_response.cookies.get_dict()
      else:
         print("login failed.")

         if not json_data['user']:
            print(f"User '{self.username}', is not found")
         elif not json_data["authenticated"]:
            print(f'Wrong password.')
         else:
            print(json_data['status'])
         
      return (self.is_authenticated, self.cookies, ua)
