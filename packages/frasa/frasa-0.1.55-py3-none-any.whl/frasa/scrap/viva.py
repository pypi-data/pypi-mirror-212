class Viva:
    ''' Base '''
    def __init__(self):
        self.main_url = 'https://news.btekno.id/antara'
        self.kanal_url = {
            'terbaru': '/terbaru', 
            'nasional': '/nasional', 
            'internasional': '/internasional', 
            'ekonomi': '/ekonomi', 
            'olahraga': '/olahraga', 
            'teknologi': '/teknologi', 
            'hiburan': '/hiburan', 
            'gayaHidup': 'gayaHidup'
        }