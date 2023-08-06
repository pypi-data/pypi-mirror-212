import json
import urllib.request

class Antara:
    ''' Base '''
    def __init__(self):
        self.rss_url = 'https://news.btekno.id/antara'
        self.topik_url = {
            'politik': '/politik', 
            'hukum': '/hukum', 
            'ekonomi': '/ekonomi', 
            'finansial': '/finansial', 
            'bisnis': '/bisnis', 
            'bursa': '/bursa', 
            'bumn': '/bumn', 
            'metro': '/metro', 
            'bola': '/bola', 
            'bola_indonesia': '/bola_indonesia', 
            'bola_internasional': '/bola_internasional', 
            'bola_inggris': '/bola_inggris', 
            'bola_spanyol': '/bola_spanyol', 
            'bola_champions': '/bola_champions', 
            'bola_italia': '/bola_italia', 
            'bola_jerman': '/bola_jerman', 
            'bola_prancis': '/bola_prancis', 
            'olahraga': '/olahraga', 
            'bulutangkis': '/bulutangkis', 
            'basket': '/basket', 
            'tenis': '/tenis', 
            'balap': '/balap', 
            'esport': '/esport', 
            'sportainment': '/sportainment', 
            'humaniora': '/humaniora', 
            'lifestyle': '/lifestyle', 
            'kuliner': '/kuliner', 
            'travel': '/travel', 
            'fashion': '/fashion', 
            'bugar': '/bugar', 
            'beauty': '/beauty', 
            'hiburan': '/hiburan', 
            'sinema': '/sinema', 
            'musik': '/musik', 
            'pentas': '/pentas', 
            'antarakustik': '/antarakustik', 
            'kpop': '/kpop', 
            'dunia': '/dunia', 
            'asean': '/asean', 
            'internasional': '/internasional', 
            'dunia_corner': '/dunia_corner', 
            'tekno': '/tekno', 
            'gadget': '/gadget', 
            'game': '/game', 
            'aplikasi': '/aplikasi', 
            'tekno_umum': '/tekno_umum', 
            'tekno_review': '/tekno_review', 
            'otomotif': '/otomotif', 
            'otomotif_umum': '/otomotif_umum', 
            'otomotif_go_green': '/otomotif_go_green', 
            'otomotif_prototype': '/otomotif_prototype', 
            'otomotif_review': '/otomotif_review', 
            'warta': '/warta', 
            'pers': '/pers'
        }
        
    ''' Terkini '''
    def terkini(self):
        url = self.rss_url + '/terbaru'
        response = urllib.request.urlopen(url)
        data = json.loads(response.read())
        return data['data']['posts']
    
    ''' Popular '''
    def popular(self):
        url = self.rss_url + '/popular'
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

