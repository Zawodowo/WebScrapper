from urllib import request
from bs4 import BeautifulSoup
import pandas as pd
from pandas import DataFrame

def getUrlList(list):
    returnList = []
    for url in list:
        req = request.urlopen(url).read().decode('UTF-8')
        soup = BeautifulSoup(req, 'html.parser')
        myul = soup.find("ul",{"class":"pagination"})
        if myul is not None:
            for itemHref in myul.find_all("a"):
                returnList.append(itemHref['href'])
        else:
            returnList.append(url)
    return returnList

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'}
l1 = []
l2 = []
l3 = []
l4 = []
l5 = []

baseUrls = ['https://styro24.pl/styropian-podlogowy-c-3/',
        'https://styro24.pl/styropian-elewacyjny-c-1/',
        'https://styro24.pl/styropian-na-fundamenty-c-4/']

urlList = getUrlList(baseUrls)

for url in urlList:
    print("Pobieram dane z: " + url + "...")
    req = request.urlopen(url).read().decode('UTF-8')
    soup = BeautifulSoup(req, 'html.parser')
    productlist = soup.find_all("div",{"class":"product column hover-light"})
    for item in productlist:
        l1.append('https://styro24.pl' + item.find("div",{"class":"image-wrapper"}).find("img")['src'])
        l2.append(item['data-name'])
        l4.append(item.find("div",{"class":"manufacturer"}).getText())
        l3.append(item.find("div",{"class":"price-wrapper"}).find("span",{"class":"price"}).getText())
        l5.append(item.find("a",{"class": "link"})['href'])


df = DataFrame({'Zdjęcie': l1, 'Nazwa': l2, 'Cena': l3, 'Producent': l4, 'Link do podstrony': l5})

df.to_excel('test.xlsx', sheet_name='styro24', index=False)
