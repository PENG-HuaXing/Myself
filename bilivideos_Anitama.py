from selenium import webdriver
from bs4 import BeautifulSoup
import re,time,requests,os
url='https://space.bilibili.com/11357018/video?tid=0&page=9&keyword=&order=pubdate'

def get_url_and_name_list(bs4):
    list=[]
    url=[]
    name=[]
    link=bs4.find_all("li",attrs={"class":"small-item"})
    for i in link:
        url.append("https:"+i.a['href'])
        name.append(i.find(attrs={'class':'title'})['title'])
    list.append(url)
    list.append(name)
    return list

def go_to_next_page():
    next=bro.find_element_by_css_selector('.be-pager-next')
    print("跳转下一页".center(100,"="))
    time.sleep(3)
    tag_class=next.get_attribute("class")
    reg=re.compile('disable')
    print("是否存在下一页，判断结果为")
    print(not bool(re.search(reg,tag_class)))
    if not bool(re.search(reg,tag_class)):
        next.click()
    return not bool(re.search(reg,tag_class))

#main function:
bro=webdriver.Chrome()
bro.get(url)
namelist=os.listdir()
while True:
    soup=BeautifulSoup(bro.page_source,'lxml')
    url_and_name=get_url_and_name_list(soup)
    #=========================================================================================
    #正则表达匹配，下载
    regular=re.compile('mad|作画(锦集|集锦|片段)|笔记',re.I)
    for i in url_and_name[1]:
        if re.search(regular,i):
            ind=url_and_name[1].index(i)
            print(i)
            for j in namelist:
                if not re.search(re.compile(i),j):
                    count=1
                else:
                    count=0
                    print("匹配了")
                    break
            print(count)
            if count==1:   #本目录下所有文件没有匹配的名字，所以count==1，进行下载，若是存在匹配文件名，则count==0，不进行下载
                print("本页面没有相匹配的文件，开始下载")
                os.system("you-get "+url_and_name[0][ind])
            else:
                print("此视频已经下载过了,不进行下载")
        else:
            continue
    #==========================================================================================
    if go_to_next_page():
        print("下一页")
        time.sleep(4)
        continue
    else:
        print("下载结束")
        break
