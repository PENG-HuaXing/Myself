
import time
import requests
import re
import os

from bs4 import BeautifulSoup
headers={'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.106 Safari/537.36','Cookie':'__cfduid=d0863dd0de1783a19b40b53db2c76ada81582354425; _danbooru2_session=8SpIdEiWg1BvMOpExRRMPYgVBtH6kg9liJi3PsPD8yZNwdlB2Rm9g6gvR8mKMVemDsaA84Qj5t0518NXQkjrONlRUFj8EbOFwkjbaDwbUmmsqi9iZzhJ730Ezryf6aE4cL1LB2NHiYkcEacGhD%2FSRcPB%2BmDsL7I%2Bt6Pp0Kdzl5t3gMbJMoQxBdscn379o%2FQVy2MFxyyTlKDrQRWJDdu9MviisARyXYiEjJrCwRtu0u9SdVgZeYNmo9kwtwjE%2F%2BT6rJtEiCYiwKTqPFiABvlBgPCFVnWxk0BcIWGkT6W9rjQxXKJUhVCU6UcFx%2By8Xwy1nFJk9OjxVDvs4AtxPpvzL9oTaJ2m4Xa6LpQ9UN9VoNaD8Lu%2BDjsdoMA%2FRN66jFtqkqpD2bOo3T%2Bcj9NOrjuLaZl46u94Sx52rSdQ7Q%3D%3D--i015u0Y67XliNWXk--b6AGYzgS8rrTSbxgOu05Ng%3D%3D; __atuvc=43%7C8%2C62%7C9; __atuvs=5e574ea1dd3f593f013'}
head={'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.106 Safari/537.36'}

baseurl='https://danbooru.donmai.us'


objurl='https://danbooru.donmai.us/posts?tags=hiten_%28hitenkei%29+&ms=1'


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
		req=reqs.get(baseurl+c['href'],headers=head)
		return BeautifulSoup(req.text)
	else:
		return None

def jump_to(parturl):
	req=reqs.get(baseurl+parturl,headers=head)
	return BeautifulSoup(req.text)

def download(bs4):
	c=bs4.find(id='post-info-size')
	os.system('wget '+c.a['href'])


html=reqs.get(objurl,headers=headers)
soup=BeautifulSoup(html.text)
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
			print('delay for 5 second'.center(191,'*'))
			time.sleep(5)
		else:
			print('It have been download!!')


	if next_page(soup):
		soup=go_to_next_page(soup) 
	else:
		break
			
