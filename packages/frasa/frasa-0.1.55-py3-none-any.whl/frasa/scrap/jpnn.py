import json
import urllib.request

class Jpnn:
    ''' Base '''
    def __init__(self):
        self.rss_url = 'https://news.btekno.id/jpnn'
        
    ''' Terkini '''
    def terkini(self):
        url = self.rss_url + '/terbaru'
        response = urllib.request.urlopen(url)
        data = json.loads(response.read())
        return data['data']['posts']