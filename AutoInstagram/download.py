import requests

class Download():

   def __init__(self, insta_id: str, local_path: str) -> None:
      self.link = 'https://instagram.com/p/' + insta_id
      self.path = local_path
   
   def download(self): # TODO
      'Download a instagram post using requests'
      post_data = requests.get(self.link + '/?__a=1')

      print(post_data.text)



