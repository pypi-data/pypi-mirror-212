import json
import urllib.request

class Tempo:
    ''' Base '''
    def __init__(self):
        self.rss_url = 'https://news.btekno.id/tempo'
        self.topik_url = {
            'nasional': '/nasional', 
            'bisnis': '/bisnis', 
            'metro': '/metro', 
            'dunia': '/dunia', 
            'bola': '/bola', 
            'cantik': '/cantik', 
            'tekno': '/tekno', 
            'otomotif': '/otomotif', 
            'seleb': '/seleb', 
            'gaya': '/gaya', 
            'travel': '/travel', 
            'difabel': '/difabel', 
            'creativelab': '/creativelab', 
            'inforial': '/inforial', 
            'event': '/event', 
        }
    
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

