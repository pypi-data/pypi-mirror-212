import json
import urllib.request

class Tribun:
    ''' Base '''
    def __init__(self):
        self.rss_url = 'https://news.btekno.id/tribun'
        self.topik_url = {
            'bisnis': '/bisnis', 
            'superskor': '/superskor', 
            'sport': '/sport', 
            'seleb': '/seleb', 
            'lifestyle': '/lifestyle', 
            'travel': '/travel', 
            'parapuan': '/parapuan', 
            'otomotif': '/otomotif', 
            'techno': '/techno', 
            'techno': '/techno'
        }
        
    ''' Terkini '''
    def terkini(self):
        url = self.rss_url + '/terbaru'
        response = urllib.request.urlopen(url)
        data = json.loads(response.read())
        return data['data']['posts']
    
    ''' Topik '''
    def topik(self, topik=None):
        if topik is None:
            return list(self.topik_url.keys())
        else:
            if topik in self.topik_url:
                url = self.rss_url + self.topik_url[topik]
                response = urllib.request.urlopen(url)
                data = json.loads(response.read())
                return data['data']['posts']
            else:
                return 'Tidak tersedia. Pastikan topik terdata di `antara.topik()`'

