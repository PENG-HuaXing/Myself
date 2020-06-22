


from bs4 import BeautifulSoup
import time,re,os,requests


headers={"User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.106 Safari/537.36"}

baseurl="https://konachan.com"
url="https://konachan.com/post?tags=vote%3A3%3APenghuaxing+order%3Avote"
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
	r=requests.get(link,headers=headers)
	f=open(name,"wb")
	f.write(r.content)
	f.close()
	print("This is downloadover"+name)

	#os.system("axel "+link)

def next_page(bs4):
	if "href" not in bs4.find(attrs={"class":"next_page"}).attrs:
		return None
	else:
		return baseurl+bs4.find(attrs={"class":"next_page"})["href"]


#main

req=requests.get(url,headers=headers)
soup=BeautifulSoup(req.text,"lxml")

namelist=os.listdir()

while True:
	link=findpost(soup)

	for i in link:
			
		bs4=jump_to(i)
		name=bs4.find_all("a",attrs={"class":re.compile("original-file-.*changed")})[-1]["href"].split("/")[-1].replace("%20"," ").replace("%28","(").replace("%29",")")
		if name in namelist:		
			print("It has been downlaod")
			print(name)
		else:
			download(bs4)
			print("delay for 3 second".center(191,"*"))
			print("now is "+soup.em.string+" page!!")
			print("="*191)
		print("next loop!!")		
	


	if next_page(soup)==None:
		break
	else:
		print("I jump to next page")
		soup=jump_to(next_page(soup))

		
	
