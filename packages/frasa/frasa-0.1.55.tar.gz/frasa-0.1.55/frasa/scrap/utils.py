import requests
import xml.etree.ElementTree as ET

# Fungsi crawler untuk mengambil konten XML dari URL
async def crawler(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        return None

# Fungsi parseRss untuk mem-parsing konten XML
async def parseRss(data):
    xml = data['xml']
    postKeys = data['postKeys']
    additionalInfo = data['additionalInfo']
    
    items = []
    root = ET.fromstring(xml)
    
    for item in root.findall('item'):
        post = {}
        for key, value in postKeys.items():
            post[key] = item.find(value).text
        
        for key, value in additionalInfo.items():
            post[key] = value
        
        items.append(post)
    
    return items