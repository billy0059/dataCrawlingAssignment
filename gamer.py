# coding:utf8
import requests
from bs4 import BeautifulSoup
import re
import xml
import codecs, json


def cleanhtml(raw_html):
	cleanr = re.compile('<.*?>')
	cleantext = re.sub(cleanr, '', raw_html)
	return cleantext
def remove_tags(text):
    return ''.join(xml.etree.ElementTree.fromstring(text).itertext())
    
page = 1 # start at page1
'''
used to save the data first in the memory
'''
data_name = [] 
data_info = []
data_yesterday_popularity = []
data_yesterday_articles = []
data_type = []
data_wannaPlay =[]
'''
use data to save tho whole data and dump into .json datatype
'''
data = {} 
data['game'] = []

while (page<10): #the value determines the pages you want to crawl

	url = "https://forum.gamer.com.tw/rank.php?page="+str(page)
	url = url + "&c=21"
	re = requests.get(url)
	content = re.text

	soup = BeautifulSoup(content,"html.parser")
	game_list = soup.find_all(class_="BH-table BH-table1")

	i=0



	for game_a in game_list[0].find_all('a'):   #for the information of pop
		if i%2==0 : # cause the second href is the target href not the first one
			url = "https://forum.gamer.com.tw/"+(game_a.get('href'))
			re = requests.get(url)
			content = re.text
			soup = BeautifulSoup(content,"html.parser")
			gameBoard = soup.find_all(class_="BH-acgbox")
			if gameBoard != [] : #if the table has value
				popularity = gameBoard[0].find_all('span')
				data_type.append(popularity[0].string)
				data_wannaPlay.append(popularity[1].string)
			
			else:
				data_type.append("NULL")
				data_wannaPlay.append("NULL")

			data_name.append(game_a.string)
		i = i+1	
	i=0
	

	for game_info in game_list[0].find_all('small'):   #for the information of pop
		data_info.append(game_info.string)


	for info in data_info :
		print(data_name[i])
		info_temp = info.split(u"?¨æ—¥äººæ°£ï¼?)[1]
		data_yesterday_popularity.append(info_temp.split(u"| ?¨æ—¥?‡ç?ï¼?)[0])
		data_yesterday_articles.append(info_temp.split(u"| ?¨æ—¥?‡ç?ï¼?)[1])
		print(data_yesterday_popularity[i])
		print(data_yesterday_articles[i])
		print(data_type[i])
		print(data_wannaPlay[i])	
		print(page)
		'''
		save the data in to a dictionary type 
		'''
		data['game'].append({
			'name' : data_name[i],
			'yesterday_popularity' : data_yesterday_popularity[i],
			'yesterday_articles' : data_yesterday_articles[i],
			'platform' : data_type[i],
			'people_wanna_play' : data_wannaPlay[i]
		})
		i = i+1
	page = page+1
'''
dump the data to the .json file
	
'''
with codecs.open('CrawlingData.json', 'w', 'utf8') as f:
     f.write(json.dumps(data, sort_keys = True, ensure_ascii=False))

