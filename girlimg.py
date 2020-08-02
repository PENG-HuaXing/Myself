import re,os,time,base64,threading
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException,NoSuchElementException

baseurl="https://girlimg.epio.app"
posturl="https://girlimg.epio.app/article"
start_page=1
end_page=7
partten=re.compile(r"(xiuren|bololi|公举殿下|rosi)",re.I)
windows_num=6
thread_list=[]



class Scrapt_page:
    def __init__(self,bs4_data):
        self.bs4_data=bs4_data
        self.postnumber=5
    def get_post(self):
        post_name=[]
        post_url=[]
        post_eles=self.bs4_data.find_all("div",attrs={"class":"ant-col-xs-24"})
        for i in post_eles:
            try:
                post_url.append(baseurl+i.div.a["href"])        #对于最后几个抓取到的class:ant-col-xs-24的div元素中并没有a tag,因此会发生AttributeError．但是此时已经抓取完成，因此可以直接跳过
                post_name.append(i.div.a.string)
            except AttributeError:
                break
        return [post_name,post_url]
    def get_img(self):
        img_url=[]
        temp_ele=self.bs4_data.find("article",attrs={"class":"article___1nKEd"}).find_all("img")
        for i in temp_ele:
            img_url.append(base64.b64decode(i['src'].split("/")[-1]).decode('utf-8').replace(".thumb.jpg",""))
        return img_url
            

def download(url_list,directory_name):
    dir_count=0
    dirlist=os.listdir()
    for i in dirlist:                                                   
        if re.search(re.compile(directory_name),i):
            dir_count=dir_count+1
        else:
            dir_count=dir_count+0
    if dir_count==1:
        print("the directory is exists")
        print("该文件 "+directory_name+" 已经存在,不进行下载......")
    elif re.search(partten,directory_name):
        print("这个文件 "+directory_name+" 不喜欢，不进行下载......")
    else:
        os.mkdir(directory_name+"_page"+str(start_page))
        os.chdir(directory_name+"_page"+str(start_page))
        for i in url_list:
            os.system("axel "+i)
        os.chdir("../")

def wait_img_OK(page_url):
    while True:
        try:
            browser.get(papge_url)
            wait=WebDriverWait(browser,10)
            wait.until(EC.presence_of_element_located((By.XPATH,"//article/div/p/img")))
            break
        except TimeoutException:
            browser.refresh()
            print("重新加载")
    return BeautifulSoup(browser.page_source,"lxml")

def wait_post_OK(papge_url):
    while True:
        try:
            browser.get(papge_url)
            wait=WebDriverWait(browser,10)
            wait.until(EC.presence_of_element_located((By.XPATH,"//div[@class='container___1F7xE']/div/div/div/div/a")))
            break
        except TimeoutException:
            browser.refresh()
            print("重新加载")
    return BeautifulSoup(browser.page_source,"lxml")

#======================================main==============================================================


#=====================================开启多个窗口进行tag页面加载======================================
for i in range(windows_num-1):
    browser.execute_script("window.open()")


for i in range(start_page,end_page+1):
    browser.switch_to.window(browser.window_handles[0])
    post_bs4=wait_post_OK(post_url+"?page"+str(start_page))
    sc=Scrapt_page(post_bs4)
    Na_url_list=sc.get_post()

#========================================================================================================
    while True
#==========================================判断剩余tag的数目，决定后续线程数目=======================================================
        if len(Na_url_list[0]) > windows_num:
            tag_num=windows_num
        else:
            tag_num=len(Na_url_list)
#===========================================================开启多线程===============================
        thread_list=[]
        for i in range(tag_num):
            browser.switch_to.window(browser.window_handles[i])
            thread_list.append(target=wait_img_OK,args=[Na_url_list[1][i]])
            thread_list[i].start()
#=================================================判断线程存活数目===========================================
        while True:
            alive_num=0
            for i in range(tag_num)：
                if thread_list[i].isAlive():
                    alive_num=alive_num+1
                else:
                    alive_num=alive_num+0
            if alive_num=0:
                break

        for i in range(tag_num):
            browser.switch_to.window(browser.window_handles[i])
            bs4_data=BeautifulSoup(browser.page_source,'lxml')
            sc_img=Scrapt_page(bs4_data)
            img_url_list=sc_img.get_img()
            download(img_url_list,Na_url_list[0][i])
            Na_url_list[0].remove(Na_url_list[0][i])
            Na_url_list[1].remove(Na_url_list[1][i])
        if len(Na_url_list[0])==0:
            break
            
