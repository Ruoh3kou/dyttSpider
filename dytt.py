import requests
from bs4 import BeautifulSoup
import re
import time

headers = {
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36",
    "Accept":"text/html, application/xhtml+xml, application/xmlq = 0.9, image/webp, image/apng, */*q = 0.8"}

class Movie:
    def __init__(self, name, Douban,link):
        self.name = name
        self.Douban = Douban
        self.link = link

    def __repr__(self):
        return '%s,豆瓣：%s分,下载地址：%s' % (self.name,self.Douban, self.link)


def getUrls(url):
    urls = []
    for x in range(1, 175):
        if x!=1:
            url = "http://www.ygdy8.net/html/gndy/dyzz/list_23_"+str(x)+".html"
        r = requests.get(url,headers=headers)
        r.encoding = 'gbk'
        soup = BeautifulSoup(r.text, 'lxml')
        tables = soup.find_all("table", class_="tbspan")
        for table in tables:
            href = table.find("a").get("href")
            urls.append("http://www.ygdy8.net"+href)
        print("Page.%d urls get." % x)
    print("All urls get.")
    return urls

def dataClean(urls):
    movies=[]
    for url in urls:
        r = requests.get(url,headers=headers)
        r.encoding = 'gbk'
        soup = BeautifulSoup(r.text, 'lxml')
        text = soup.find("div", id="Zoom").get_text(strip=True)
        DBmark = re.findall(r"评分　(.+?)/10", text)
        if len(DBmark)>=1 and float(DBmark[0])>=8:
            try:
                name = re.findall(r"片　　名　(.+?)◎", text)[0]
                link = soup.find("div", id="Zoom").find("a").get("href")
                movie=Movie(name,DBmark[0],link)
                movies.append(movie)
            except:
                print("dataClean - save error.")
        time.sleep(3)
    print("movies get.")
    return movies

def dataSave(movies):
    f = open('data.txt', 'a')
    for movie in movies:
        movie_items = str(movie).split(',')      
        f.writelines([line+'\n' for line in movie_items])
        f.write('=============================\n')
    f.close()
    print("its ok")

if __name__ == '__main__':
    startUrl = "http://www.ygdy8.net/html/gndy/dyzz/index.html"
    urls = getUrls(startUrl)
    data = dataClean(urls)
    dataSave(data)
