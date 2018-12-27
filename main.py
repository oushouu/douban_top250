#爬取豆瓣top250电影并制成dataframe
import requests, bs4
import pandas as pd
from urllib.request import quote
from download import movie_download

start_id = 0
m_name_ch = []
m_name_en = []
m_name_ot = []
m_star = []
m_people = []
m_quote = []
m_info = []
m_url = []
col_name = ['电影名','原名','其他翻译', '豆瓣评分', '评价人数', '简述', '基本信息', 'url']

while start_id < 250:
    url = 'https://movie.douban.com/top250?start=' + str(start_id) + '&filter='
    douban = requests.get(url)
    bsdouban = bs4.BeautifulSoup(douban.text, 'html.parser')
    
    #获取电影名和链接
    link = bsdouban.select('li div div div a')
    for movie in link:
        m_url.append(movie.get('href'))
        m_name_ch.append(movie.select('.title')[0].get_text())
        if len(movie.select('.title')) > 1:
            m_name_en.append(movie.select('.title')[1].get_text().replace('\xa0/\xa0', ''))# ' / '里的空格不是普通空格，其实是‘\xa0’
        else:
            m_name_en.append(None)
        m_name_ot.append(movie.select('.other')[0].get_text().replace('\xa0', ''))
        
    #获取评分 
    link2 = bsdouban.select('.star')
    for rate in link2:
        m_star.append(rate.select('.rating_num')[0].get_text())
        m_people.append(rate.select('span')[3].get_text().rstrip('人评价'))
    
    #获取一句话简介    
    link3 = bsdouban.select('.quote')
    for quote in link3:
        m_quote.append(quote.select('span')[0].get_text())
        
    #获取电影信息
    link4 = bsdouban.select('.info .bd')
    for information in link4:
        info = information.select('p')[0].get_text()
        content = info.strip('\n ').replace('\xa0', '').replace('\n', '').replace(' ', '')
        m_info.append(content)
    
    #下一页
    start_id += 25 

 #将各个list组合中dataframe
data = list(zip( m_name_ch, m_name_en, m_name_ot, m_star, m_people, m_quote, m_info, m_url))
df = pd.DataFrame(data, columns = col_name)
df

#将数据导出至excel
df.to_excel('豆瓣top250电影数据.xlsx', index = True, encoding = 'utf-8')

#打印top250的电影下载链接，或返回无结果提示
for movie in m_name_ch:
    movie_download(movie)
