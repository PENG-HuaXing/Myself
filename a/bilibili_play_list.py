from bs4 import BeautifulSoup 
from selenium import webdriver
import re,os,time
baseurl='https://www.bilibili.com'
url="https://www.bilibili.com/video/BV1o4411t7yA"
bro=webdriver.Chrome()
bro.get(url)
time.sleep(10)#暂停五秒，否则无法获得播放列表的html文本
soup=BeautifulSoup(bro.page_source,'lxml')
playlist=soup.find('ul',attrs={"class":"list-box"})
videos=playlist.find_all('a')
videos_href=[]
videos_name=[]
for i in videos:
    videos_href.append(baseurl+i['href'])
    videos_name.append(i['title'])
print(videos_href)
print(videos_href)
list_name=os.listdir()
for i in videos_name:
    reg=re.compile(i)
    for j in list_name:
        if re.search(reg,j):
            count=0
            break
        else:
            count=1
    if count==0:
        print("这个文件已经下载过了，不再进行下载")
    else:
        os.system('you-get '+videos_href[videos_name.index(i)])
            
