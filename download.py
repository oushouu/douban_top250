import requests, bs4, webbrowser
from urllib.request import quote

#定义一个一键下片函数
def movie_download(movie_name):
    url = 'http://s.ygdy8.com/plus/so.php?typeid=1&keyword=' + quote(movie_name.encode('gbk'))
    page1 = requests.get(url)
    bspage1 = bs4.BeautifulSoup(page1.content, 'html.parser')
    link = bspage1.select('.co_content8 ul b a')
    #print(link[0].get('href'))
    try:
        url2 = 'https://www.ygdy8.com' + link[0].get('href')
        #print(url2)
    except IndexError:
        print('抱歉，没有找到您要的片儿 + "' + movie_name + '"')    
    else:    
        page2 = requests.get(url2)
        bspage2 = bs4.BeautifulSoup(page2.content, 'html.parser')
        link2 = bspage2.select('table tbody tr a')
        print(movie_name + '的下载链接')
        for download in link2:
            print(download.get('href') + '\n')
            download_link = download.get('href')
        #webbrowser.open(download_link)
