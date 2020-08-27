import re,os,time,base64,threading
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException,NoSuchElementException

baseurl="https://girlimg.epio.app"
posturl="https://girlimg.epio.app/article"
start_page=46
end_page=100
partten=re.compile(r"(xiuren|mygirl|bololi|原来是茜公举殿下|少女映画|小鸟酱|新蔻|rosi)",re.I)
windows_num=5
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
        print("post href抓取完成")
        return [post_name,post_url]
    def get_img(self):
        img_url=[]
        while True:
            try:
                temp_ele=self.bs4_data.find("article",attrs={"class":"article___1nKEd"}).find_all("img")
                break
            except AttributeError:
                browser.refresh()
                time.sleep(60)

        for i in temp_ele:
            try:
                img_url.append(base64.b64decode(i['src'].split("/")[-1]).decode('utf-8').replace(".thumb.jpg",""))
            except:
                img_url.append(i['src'])            #会出现并没有用base64编码的图片元地址，会出现binascii.Error: Incorrect padding错误
        print("img src抓取完成")
        return img_url
            

def download(url_list,directory_name):
    directory_name=directory_name.replace("/","_")                          #有的文件名称存在反斜杠，系统无法识别
    reg_filename=directory_name.replace("[","\[").replace("]","\]").replace("(","\(").replace(")","\)")              #有的文件名字中存在中括号，需要转移后进行正则表达匹配
    dir_count=0
    dirlist=os.listdir()
    for i in dirlist:                                                   
        if re.search(re.compile(reg_filename),i):
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
        print("创建"+directory_name+"文件夹")
        ff=open("url.log","w")
        for i in url_list:
            ff.write(i+"\n")
        ff.close()
        for i in url_list:
            os.system("axel "+i)
        os.chdir("../")

def wait_img_OK(page_url,winnum):
    while True:
        try:
            browser.get(page_url)
            wait=WebDriverWait(browser,130)
            print("窗口"+str(winnum)+"等待130S"+"\n"+page_url)
            wait.until(EC.presence_of_element_located((By.XPATH,"//article[@class='article___1nKEd']/div/p/img")))
            time.sleep(2)                                               #猜测可能找到相应的元素后由于不知什么原因又暂时消失了
            print("已经找到对应元素")
            #============================================================================
            try:
                test=BeautifulSoup(browser.page_source,'lxml')
                test.find("article",attrs={"class":"article___1nKEd"}).find_all("img")
            except AttributeError:
                print("出现异常，找不到find_all(’img‘)标签属性")
                f1=open("加载ERROR页面.log"+str(winnum),"w")
                errorpage=BeautifulSoup(browser.page_source,"lxml")
                f1.write(test.prettify()+"\n\n\n\n"+100*"=")
                f1.write(errorpage.prettify())
                f1.close()
            #============================================================================
            break
        except TimeoutException:

            print("窗口"+str(winnum)+"重新加载"+"\n"+page_url)
            browser.switch_to.window(browser.window_handles[winnum])
            browser.refresh()
    return BeautifulSoup(browser.page_source,"lxml")

def wait_post_OK(page_url):
    while True:
        try:
            browser.get(page_url)
            wait=WebDriverWait(browser,130)
            print("等待130S\n"+page_url)
            wait.until(EC.presence_of_element_located((By.XPATH,"//div[@class='container___1F7xE']/div/div/div/div/a")))
            print("已经找到对应元素")
            break
        except TimeoutException:
            print("重新加载\n"+page_url)
            browser.refresh()
            
    return BeautifulSoup(browser.page_source,"lxml")

#======================================main==============================================================
browser=webdriver.Chrome()

#=====================================开启多个窗口进行tag页面加载======================================
for i in range(windows_num-1):
    browser.execute_script("window.open()")


for i in range(start_page,end_page+1):
    browser.switch_to.window(browser.window_handles[0])
    post_bs4=wait_post_OK(posturl+"?page="+str(i))
    sc=Scrapt_page(post_bs4)
    Na_url_list=sc.get_post()
#=================================================写入文件=========================================
    log_file=open("page"+str(start_page)+".log","a")
    for i in range(len(Na_url_list[0])):
        log_file.write(Na_url_list[0][i]+"\t\t"+"\n")
    log_file.close()
#========================================================================================================
    while True:
        print("抓取到的tag数目为："+str(len(Na_url_list[0])))
#==========================================判断剩余tag的数目，决定后续线程数目=======================================================
        if len(Na_url_list[0]) > windows_num:
            tag_num=windows_num
        else:
            tag_num=len(Na_url_list[0])
#===========================================================开启多线程===============================
        thread_list=[]
        for i in range(tag_num):
            print("切换到窗口"+str(i))
            browser.switch_to.window(browser.window_handles[i])
            thread_list.append(threading.Thread(target=wait_img_OK,args=[Na_url_list[1][i],i]))
            print("第"+str(i)+"线程开始")
            thread_list[i].start()
#=================================================判断线程存活数目===========================================
        while True:
            alive_num=0
            for i in range(tag_num):
                time.sleep(5)
                if thread_list[i].isAlive():
                    print("第"+str(i)+"线程存活")
                    alive_num=alive_num+1
                else:
                    print("第"+str(i)+"线程over")
                    alive_num=alive_num+0

            if alive_num==0:
                print("全部线程结束")
                break

        for i in range(tag_num):
            ff=open("fuck.log","a")
            ff.write("windows"+str(i)+"\t"+Na_url_list[0][i]+"\t"+Na_url_list[1][i]+"\n")
            ff.close()

        for i in range(tag_num):
            browser.switch_to.window(browser.window_handles[i])
            while True:
                try:
                    bs4_data=BeautifulSoup(browser.page_source,'lxml')
                    break
                except TimeoutException:
                    print("加载超时!!!!")
                    browser.refresh()
                    time.sleep(50)
                    print("暂停50S")
            while True:
                try:
                    sc_img=Scrapt_page(bs4_data)
                    img_url_list=sc_img.get_img()
                    if len(img_url_list)==0:
                        raise AttributeError
                    else:
                        break
                except AttributeError:
                    print("未知属性错误：NoneType object has no attribute find_all")
                    browser.refresh()
                    time.sleep(60)
                    bs4_data=BeautifulSoup(browser.page_source,"lxml")
#==========================================================================================================
#            info_file=open("url","w")
#            info_file.write(browser.current_url)
#            info_file.close()
#=========================================================================================================
            download(img_url_list,Na_url_list[0][i])
#========================================删除已经完成的post=================================================
        for i in range(tag_num):
            Na_url_list[0].remove(Na_url_list[0][0])
            Na_url_list[1].remove(Na_url_list[1][0])
        
#        file_temp=open(str(len(Na_url_list[0])),"w")
#        for i in Na_url_list[0]:
#            file_temp.write(i+"\n")
#        file_temp.close()

        if len(Na_url_list[0])==0:
            start_page=start_page+1
            break
            

