#encoding=utf-8

import requests,os,re,time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException,NoSuchElementException 



def findpost(bs4):									#找到当前页面的post标签超链接，并返回一个超链接列表
	post=bs4.find_all(attrs={"class":"album-card"}) 
	url=[]
	for i in post:
		if "href" not in i.a.attrs:					#失效的超链接
			print("This album is over!!")
		else:
			url.append("https:"+i.a["href"])
	return url

def jump_to_obtain_imglink(url):					#输入post超链接，并进入，搜索图片源链接并返回一个源链接列表
	broswer.execute_script("window.open()")
	broswer.switch_to.window(broswer.window_handles[1])
	broswer.get(url)
	while True:
		try:
			wait=WebDriverWait(broswer,5)
			element=wait.until(EC.presence_of_element_located((By.XPATH,'//div[@class="images"]/img')))
			break
		except TimeoutException:
			print("请等待")
			
	 
	#time.sleep(3)
	html=broswer.page_source
	broswer.close()
	broswer.switch_to.window(broswer.window_handles[0])
	cc=BeautifulSoup(html,"lxml").find_all("div",attrs={"class":"images"})
	l=cc[0].find_all("img")
	link=[]
	for i in l:
		link.append(i["data-photo-imager-src"])
	return link

def next_page():												#检查是否存在下一页按钮并click。要注意的是存在中文字符比较，由于selenium返回的是utf8字符
	ss=broswer.find_elements_by_css_selector(".panigation")		#所以本文汉字编码也必须是utf8格式，否则无法匹配
	count=0														#另外在跳转页面由于是Ajix技术，所以要等待整体框架加载完成后再获取当前页面源码
	print("execute next page!!")
	for i in ss:
		if i.text=="下一页":
			i.click()
			time.sleep(10)
			count=count+1
		else:
			count=count+0
	return count
	

#main
broswer=webdriver.Chrome()
broswer.get("https://passport.bilibili.com/login")

print("Please longin __ if you have done Please imput \"1\"")

s=input()
if s=="1":
    broswer.get("https://space.bilibili.com/16021397/album")

print("Please clear the window--if you have clean it ,Please input 1")
input()
thispagelink=[]
namelist=os.listdir()

while True:
	soup=BeautifulSoup(broswer.page_source,"lxml")
	link1=findpost(soup)
	for i in link1:
		print(i)
		inner=jump_to_obtain_imglink(i)
		thispagelink.append(inner)
	for i in thispagelink:
		for j in i:
			if j.split("/")[-1] in namelist:
				print("这个文件已经下载过了！！")
			else:
				print("这个文件是第一次下载")
				os.system("wget "+j)
	thispagelink=[]
	if next_page()==1:
		print("Jump to next page!!!")
		print("*"*191)
	else:
		print("There is no next page")
		break			
