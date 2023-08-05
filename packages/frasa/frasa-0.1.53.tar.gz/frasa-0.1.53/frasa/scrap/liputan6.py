from requests import get
from urllib.parse import urlsplit
from bs4 import BeautifulSoup
import re, datetime

class Liputan6:
    '''
        Base
    '''
    def __init__(self):
        self.news_url = 'https://liputan6.com'
        self.tag_url = '/tag/'
        self.search_url = '/search'
        self.indeks_url = '/indeks'
        self.popular_url = '/indeks/terpopuler'
        self.kanal_url = {
            'news': '/news', 
            'pemilu': '/pemilu', 
            'bisnis': '/bisnis', 
            'bola': '/bola', 
            'crypto': '/crypto', 
            'showbiz': '/showbiz', 
            'tekno': '/tekno', 
            'cek-fakta': 'cek-/fakta', 
            'citizen6': '/citizen6', 
            'saham': '/saham', 
            'regional': '/regional', 
            'otomotif': '/otomotif', 
            'disabilitas': '/disabilitas', 
            'global': '/global', 
            'on-off': 'on-/off', 
            'surabaya': '/surabaya', 
            'lifestyle': '/lifestyle', 
            'health': '/health', 
            'video': '/video', 
            'jatim': '/jatim', 
            'jateng': '/jateng', 
        }
    
    def soup(self, url):
        return BeautifulSoup(url.text, 'html.parser')
    
    '''
        Indeks News
    '''
    def build_indeks_url(self, kanal: str, tanggal: str, page: int):
        qs1 = '/'+tanggal
        qs2 = '?page='+str(page)
        return self.news_url + kanal + self.indeks_url + qs1 + qs2

    def indeks(self, kanal = '', tanggal = datetime.date.today().strftime("%Y-%m-%d"), page=1, multi_page=False):
        url_dict = self.kanal_url
        kanal = url_dict.get(kanal, '/news')
        tanggal = datetime.datetime.strptime(tanggal, "%Y-%m-%d")
        tanggal = tanggal.strftime("%Y/%m/%d")
        if multi_page is True:
            return self.indeks_multi_page(kanal, tanggal, page)
        else:
            url = self.build_indeks_url(kanal, tanggal, page)
            return self.indeks_crawl(url)
        
    def indeks_crawl(self, url):
        data = get(url)
        news = self.soup(data).find('div', attrs={"data-component-name": "desktop:articles:list"})
        ini = news.find_all('article', attrs={"data-component-name": "desktop:articles:list:item"})
        key  = 0
        parse_data = list()
        for i in ini:
            key += 1
            title = i.find_all('a', attrs={"data-template-var": "url"})[1].text
            link = i.find('a', attrs={"data-template-var": "url"}).get('href')
            image = i.find('img', attrs={"data-template-var": "image"}).get('src')
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
        qs = f'?q={query}'
        qs2 = '&order=latest&channel_id=&from_date=&to_date=type=all'
        return self.news_url + self.search_url + qs + qs2 + "&page=" + str(page)

    def cari(self, query, page=1, multi_page=False):
        if multi_page is True:
            return self.news_multi_page(query, page)
        else:
            url = self.build_search_url(query, page)
            return self.news_crawl(url)

    def news_crawl(self, url, detail=False):
        data = get(url)
        news = self.soup(data).find('section', attrs={"data-component-name": "desktop:box"})
        ini = news.find_all('article', attrs={"data-component-name": "desktop:search-results:articles:iridescent-list:text-item"})
        return ini
        data = []
        for i in ini:
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
        