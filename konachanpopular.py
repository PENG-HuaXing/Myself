


from bs4 import BeautifulSoup
import time,re,os,requests,datetime



headers={"User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.106 Safari/537.36"}

baseurl="https://konachan.com"

delday=datetime.timedelta(days=1)

delweek=datetime.timedelta(days=7)

def popular_time(datetime):
        date=datetime
        while True:
                if date.strftime("%w")=="1":
                        break
                else:
                        date=date-delday
        return date
print("现在是星期："+popular_time(datetime.datetime.now()).strftime("%w"))



def popular_time_url(datetime):
        url='https://konachan.com/post/popular_by_week?day='+str(datetime.day)+'&month='+str(datetime.month)+'&year='+str(datetime.year)
        return url
print(popular_time_url(popular_time(datetime.datetime.now())))        






def findpost(bs4):
	link=[]	
	c=bs4.find_all("li",attrs={"id":re.compile("p\d+")})
	for i in c:
		link.append(baseurl+i.div.a["href"])
	return link
	
def jump_to(url):
	return BeautifulSoup(requests.get(url,headers=headers).text,"lxml")


def download(bs4):
	link=bs4.find_all("a",attrs={"class":re.compile("original-file-.*changed")})[-1]["href"]
	name=bs4.find_all("a",attrs={"class":re.compile("original-file-.*changed")})[-1]["href"].split("/")[-1].replace("%20"," ").replace("%28","(").replace("%29",")")
	print("now download is "+name)
	if name in os.listdir():
		print("I will redownload")
	else:
		print("It is my first time to download it")
	#r=requests.get(link,headers=headers)
	#f=open(name,"wb")
	#f.write(r.content)
	#f.close()
	print("This is downloadover"+name)

	os.system("axel "+link)

#main

'''
req=requests.get(url,headers=headers)
soup=BeautifulSoup(req.text,"lxml")

olddate=datetime.datetime(2019,3,4)

namelist=os.listdir()
count=0
'''

namelist=os.listdir()
enddate=datetime.datetime(2019,3,4)
startdate=datetime.datetime(2019,5,4)
date=popular_time(startdate)
while True:
        dirname=date.strftime("%B %d,%Y")+"-"+(date-delweek).strftime("%B %d,%Y")

        if dirname not in namelist:
                os.mkdir(dirname)
                print("已经创建"+dirname+"文件夹")
                url=popular_time_url(date)
                print("本次进入的链接为")
                print(url)

                soup=BeautifulSoup(requests.get(url).text)
        else:
                print("这个日期的已经下载过了,直接进入下一个循环")
                date=date-delweek
                continue
        os.chdir(dirname)
        print("已经切换到相应目录")
        print(url)
        f=open("url.txt","w")
        f.write(url)
        f.close()
        print("已经生成相应文件")

        link=findpost(soup)

        #下载部分=======================================================
        for i in link:
            bs4=jump_to(i)
            name=bs4.find_all("a",attrs={"class":re.compile("original-file-.*changed")})[-1]["href"].split("/")[-1].replace("%20"," ").replace("%28","(").replace("%29",")")
            if name in namelist:
                print("It has been downlaod")
                print(name)
                time.sleep(5)
            else:
                download(bs4)
                print("delay for 10 second".center(191,"*"))
                time.sleep(10)
                #print("now is "+soup.em.string+" page!!")
                print("="*191)
        print("next loop!!,time sleep 150 seconds")
        time.sleep(150)
        #下载部分=======================================================
        
        
        os.chdir("..")
        if date<enddate:
                break
        else:
                date=date-delweek
                print("下一个循环")
