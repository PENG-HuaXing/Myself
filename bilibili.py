#encoding=utf-8

import requests,os,re,time

from bs4 import BeautifulSoup
from selenium import webdriver



def findpost(bs4):
	post=bs4.find_all(attrs={"class":"album-card"}) 
	url=[]
	for i in post:
		if "href" not in i.a.attrs:
			print("This album is over!!")
		else:
			url.append("https:"+i.a["href"])
	return url

def jump_to_obtain_imglink(url):
	broswer.execute_script("window.open()")
	broswer.switch_to.window(broswer.window_handles[1])
	broswer.get(url)
	html=broswer.page_source
	broswer.close()
	broswer.switch_to.window(broswer.window_handles[0])
	cc=BeautifulSoup(html,"lxml").find_all("div",attrs={"class":"images"})
	l=cc[0].find_all("img")
	link=[]
	for i in l:
		link.append(i["data-photo-imager-src"])
	return link
def next_page():
	ss=broswer.find_elements_by_css_selector(".panigation")
	count=0
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
    broswer.get("https://space.bilibili.com/36163672/favlist?fid=albumfav")

print("Please clear the window--if you have clean it ,Please input 1")
input()
thispagelink=[]

while True:
	soup=BeautifulSoup(broswer.page_source,"lxml")
	link1=findpost(soup)
	for i in link1:
		print(i)
		inner=jump_to_obtain_imglink(i)
		thispagelink.append(inner)
	for i in thispagelink:
		for j in i:
			os.system("wget "+j)
	thispagelink=[]
	if next_page()==1:
		print("Jump to next page!!!")
		print("*"*191)
	else:
		print("There is no next page")
		break			
