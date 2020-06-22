
import time
import requests
import re
import os
from requests.exceptions import ConnectionError

from bs4 import BeautifulSoup
headers={'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.106 Safari/537.36','Cookie':'__cfduid=d0863dd0de1783a19b40b53db2c76ada81582354425; _danbooru2_session=8SpIdEiWg1BvMOpExRRMPYgVBtH6kg9liJi3PsPD8yZNwdlB2Rm9g6gvR8mKMVemDsaA84Qj5t0518NXQkjrONlRUFj8EbOFwkjbaDwbUmmsqi9iZzhJ730Ezryf6aE4cL1LB2NHiYkcEacGhD%2FSRcPB%2BmDsL7I%2Bt6Pp0Kdzl5t3gMbJMoQxBdscn379o%2FQVy2MFxyyTlKDrQRWJDdu9MviisARyXYiEjJrCwRtu0u9SdVgZeYNmo9kwtwjE%2F%2BT6rJtEiCYiwKTqPFiABvlBgPCFVnWxk0BcIWGkT6W9rjQxXKJUhVCU6UcFx%2By8Xwy1nFJk9OjxVDvs4AtxPpvzL9oTaJ2m4Xa6LpQ9UN9VoNaD8Lu%2BDjsdoMA%2FRN66jFtqkqpD2bOo3T%2Bcj9NOrjuLaZl46u94Sx52rSdQ7Q%3D%3D--i015u0Y67XliNWXk--b6AGYzgS8rrTSbxgOu05Ng%3D%3D; __atuvc=43%7C8%2C62%7C9; __atuvs=5e574ea1dd3f593f013'}
head={'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.106 Safari/537.36'}

baseurl='https://danbooru.donmai.us'


objurl='https://danbooru.donmai.us/posts?ms=1&page=2&tags=morikura_en+'


reqs=requests.Session()

def next_page(bs4):
	c=bs4.find('a',attrs={'rel':'next'})
	if c==None:
		return False
	else:
		return True
def go_to_next_page(bs4):
	if next_page(bs4):
		c=bs4.find('a',attrs={'rel':'next'})
		while True:		
			try:
				req=reqs.get(baseurl+c['href'],headers=head)
				break
			except ConnectionError:
				print("连接错误，请等待２０ｓ")
				time.sleep(20)
		return BeautifulSoup(req.text,"lxml")
	else:
		return None

def jump_to(parturl):
	while True:		
		try:
			req=reqs.get(baseurl+parturl,headers=head)
			break
		except ConnectionError:
			print("连接错误，请等待２０ｓ")
			time.sleep(20)
	return BeautifulSoup(req.text,"lxml")

def download(bs4):
	c=bs4.find(id='post-info-size')
	os.system('axel '+c.a['href'])

count=0
html=reqs.get(objurl,headers=headers)
soup=BeautifulSoup(html.text,"lxml")
name=os.listdir()
while True:

	s=[]
	c=soup.find_all(id=re.compile('post_\d+'))
	page=soup.find(attrs={'class':'current-page'})
	print('*'*191)
	print('now is '+page.span.string+' page')
	print('*'*191)

	for i in c:
		bs4=jump_to(i.a['href'])
		namelink=bs4.find(id='post-info-size')
		realname=namelink.a['href'].split(sep='/')[-1]
		if realname not in name:
			download(bs4)
			print('*'*191)
			print('now is '+page.span.string+' page')
			print('*'*191)
			print('delay for 10 second'.center(191,'*'))
			time.sleep(10)
			count=-1
		else:
			if count==-1:
				count=0
				count+=1
			else:
				count+=1
			print('It have been download!!'+str(count))
		if count>=5:
			break
	if count>=5:
		break
	print("This page has been download +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++Please wait for 200 second")
	time.sleep(200)

	if next_page(soup):
		soup=go_to_next_page(soup) 
	else:
		break
			
