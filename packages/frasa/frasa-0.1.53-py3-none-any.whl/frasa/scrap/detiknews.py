from requests import get
from urllib.parse import urlsplit
from bs4 import BeautifulSoup
from frasa.base import slugify
import re, datetime

class Detiknews:
    '''
        Base
    '''
    def __init__(self):
        self.news_url = 'https://news.detik.com'
        self.popular_url = 'https://www.detik.com/terpopuler/'
        self.tag_url = 'https://www.detik.com/tag/'
        self.search_url = 'https://www.detik.com/search/searchall?'
        self.indeks_url = '/indeks'
    
    def soup(self, url):
        return BeautifulSoup(url.text, 'html.parser')
    
    '''
        Indeks News
    '''
    def build_indeks_url(self, kanal: str, tanggal: str, page: int):
        qs1 = '/'+str(page)
        qs2 = '?date='+tanggal
        return kanal + self.indeks_url + qs1 + qs2

    def indeks(self, kanal = '', tanggal = datetime.date.today().strftime("%Y-%m-%d"), page=1, multi_page=False):
        url_dict = {
            'news': 'https://news.detik.com',
            'edu': 'https://www.detik.com/edu',
            'finance': 'https://finance.detik.com',
            'hot': 'https://hot.detik.com',
            'sport': 'https://sport.detik.com',
            'sepakbola': 'https://sport.detik.com/sepakbola',
            'oto': 'https://oto.detik.com',
            'food': 'https://food.detik.com',
            'health': 'https://health.detik.com'
        }
        
        kanal = url_dict.get(kanal, 'https://news.detik.com')

        tanggal = re.sub(r'(\d{4})-(\d{2})-(\d{2})', r'\2/\3/\1', tanggal)
        tanggal = tanggal.replace('/', '%2F')
        if multi_page is True:
            return self.indeks_multi_page(kanal, tanggal, page)
        else:
            url = self.build_indeks_url(kanal, tanggal, page)
            return self.indeks_crawl(url)
        
    def indeks_crawl(self, url):
        data = get(url)
        news = self.soup(data).find('div', class_='indeks')
        ini = news.find_all('article')
        key  = 0
        parse_data = list()
        for i in ini:
            key += 1
            title = i.find_all('a', class_='media__link')[1].text
            link = i.find('a', class_='media__link').get('href')
            image = i.find_all('a', class_='media__link')[0].img['src']
            parse_data.append({'title': title, 'link': link, 'image': image})
        return parse_data

    def indeks_multi_page(self, kanal, tanggal, page):
        all_results = []
        for page in range(1, page+1):
            url = self.build_indeks_url(kanal, tanggal, page)
            search_result = self.indeks_crawl(url)
            all_results.extend(search_result)
            
        return {"status": 200, "data": all_results, "length": len(all_results)}
    
    '''
        Search
    '''
    def build_search_url(self, query: str, page: int):
        qs = f'query={query}'
        qs2 = '&siteid=3&sortby=time&sorttime=0&page='
        return self.search_url + qs + qs2 + str(page)

    def cari(self, query, page=1, multi_page=False):
        if multi_page is True:
            return self.news_multi_page(query, page)
        else:
            url = self.build_search_url(query, page)
            return self.news_crawl(url)

    def news_crawl(self, url, detail=False):
        data = get(url)
        news = self.soup(data).find_all('article')
        data = []
        for i in news:
            judul = i.find('h2').text
            link = i.find('a').get('href')
            gambar = i.find('img').get('src')
            preview = i.find('p').text
            body = ''
            if detail:
                body = detail(link)
            waktu = i.find('span', class_="date").text
            data.append({'judul': judul, 'link': link, 'gambar': gambar, 'preview': preview, 'body': body, 'waktu': waktu})
        return data

    def news_multi_page(self, query, count = 1):
        all_results = []
        for count in range(1, count+1):
            url = self.build_search_url(query, count)
            search_result = self.news_crawl(url)
            all_results.extend(search_result)
        return {"status": 200, "data": all_results, "length": len(all_results)}
    
    '''
        Kanal
    '''
    def kanal(self):
        data = get(self.news_url)
        listCategory = self.soup(data).find('ul', class_='nav--column-2').find_all('a')
        list_kamu = list()
        for i in listCategory:
            title = i.text.strip()
            link = i.get('href')
            list_kamu.append({'title': title, 'slug': slugify(title), 'link': link})
        return list_kamu
    
    '''
        Popular
    '''
    def build_popular_url(self, query: str):
        return self.popular_url + query
    
    def popular(self, kanal=''):
        url = self.build_popular_url(kanal)
        data = get(url)
        news = self.soup(data).find('div', class_='indeks')
        ini = news.find_all('article', class_='list-content__item')
        key  = 0
        parse_data = list()
        for i in ini:
            key += 1
            title = i.find_all('a', class_='media__link')[1].text
            link = i.find('a', class_='media__link').get('href')
            image = i.find_all('a', class_='media__link')[0].img['src']
            parse_data.append({'title': title, 'link': link, 'image': image})
        return parse_data
    
    '''
        Hashtag
    '''
    def build_tag_url(self, query: str, page: int):
        parameter = '/?sortby=time&page='
        return self.tag_url + slugify(query) + parameter + str(page)
    
    def tag(self, query, page=1, multi_page=False):
        if multi_page is True:
            return self.multi_page(query, page)
        else:
            url = self.build_tag_url(query, page)
            return self.tag_crawl(url)
        
    def tag_crawl(self, url):
        data = get(url)
        news = self.soup(data).find('div', class_='list-berita')
        ini = news.find_all('article')
        key  = 0
        parse_data = list()
        for i in ini:
            key += 1
            title = i.find('h2', class_='title').text
            link = i.find('a').get('href')
            image = i.find('img')['src']
            preview = i.find('p').text
            parse_data.append({'title': title, 'link': link, 'image': image, 'preview': preview})
        return parse_data
    
    def multi_page(self, query, count = 1):
        all_results = []
        for count in range(1, count+1):
            url = self.build_tag_url(query, count)
            search_result = self.tag_crawl(url)
            all_results.extend(search_result)
        return {"status": 200, "data": all_results, "length": len(all_results)}
    
    '''
        Detail
    '''
    def build_detail_url(self, url: str):
        a = urlsplit(url)
        qs = 'single=1'
        return a.scheme + '://' + a.netloc + a.path + '?' + qs

    def detail(self, url: str) -> str:
        data = get(self.build_detail_url(url))
        article = self.soup(data).find('article', class_='detail')
        title = article.find('h1', class_='detail__title').text.strip()
        if title == '':
            return { 'code': 404, 'message': 'Not Found' }
        
        date = article.find('div', class_='detail__date').text.strip()
        author = article.find('div', class_='detail__author').text.strip()
        image = article.find_all('img')[0]['src']
        desc = article.find('div', class_='detail__body-text')
        detail_dec = desc.find_all('p')
        detail = list()
        for i in detail_dec:
            if i.text.strip() != "ADVERTISEMENT" and i.text.strip() != "SCROLL TO RESUME CONTENT":
                detail.append(i.text.strip())   

        tag_fol = article.find_all('a', attrs={'dtr-act': 'tag'})
        tag = list()
        for i in tag_fol:
            tag.append(i.text.strip())
        return {'title': title, 'date': date, 'detail': detail, 'tag': tag, 'image': image, 'author': author}
        