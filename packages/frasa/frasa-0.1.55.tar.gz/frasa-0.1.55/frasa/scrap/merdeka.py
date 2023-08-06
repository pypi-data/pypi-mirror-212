import json
import urllib.request

class Merdeka:
    ''' Base '''
    def __init__(self):
        self.rss_url = 'https://news.btekno.id/merdeka'
        self.topik_url = {
            'terbaru': '/terbaru', 
            'jakarta': '/jakarta', 
            'dunia': '/dunia', 
            'gaya': '/gaya', 
            'olahraga': '/olahraga', 
            'teknologi': '/teknologi', 
            'otomotif': '/otomotif', 
            'khas': '/khas', 
            'sehat': '/sehat', 
            'jateng': '/jateng'
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

