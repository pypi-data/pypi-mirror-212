import json
import urllib.request

class Kumparan:
    ''' Base '''
    def __init__(self):
        self.rss_url = 'https://news.btekno.id/kumparan'
        
    ''' Terkini '''
    def terkini(self):
        url = self.rss_url + '/terbaru'
        response = urllib.request.urlopen(url)
        data = json.loads(response.read())
        return data['data']['posts']