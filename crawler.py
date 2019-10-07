import requests
from bs4 import BeautifulSoup
import bs4
import re
import os

def crawl_quora_topics(topic):
	topic='-'.join(topic.split(' '))
	script_dir = os.getcwd()
	rel_path = "saidas/"+topic+".txt"
	abs_file_path = os.path.join(script_dir, rel_path)
	#if not os.path.exists(abs_file_path):
	#	os.mkdir(abs_file_path)
	print(topic)
	url='https://pt.quora.com/topic/'+topic;
	source_code=requests.get(url)
	plain_text=source_code.text
	soup=BeautifulSoup(plain_text,'html.parser')
	i=0
	file = open(abs_file_path,"a", encoding='utf-8')
	file.write('\"id\",\"question\", \"answers\"')
	file.write('\n')
	print(len(soup.find_all('a',{'class':'question_link'})))
	#if(len(soup.find_all('a',{'class':'question_link'})) == 0)
	#	print('cooldown')
	for question in soup.find_all('a',{'class':'question_link'}):
		a=''
		print('\n')
		print('**************************NEW QUESTION************************************')
		if(i<100):
			i=i+1
			print(i)
			print('\n')
			file.write('\"'+str(i)+'\",')
			print(question.span.get_text())
			file.write('\"'+question.span.get_text()+'\",')
			url=question.get('href')
			print(url)
			source_code=requests.get(url)
			plain_text=source_code.text
			ansSoup=BeautifulSoup(plain_text,'html.parser')
			txtAnswer=""
			for answer in ansSoup.find_all('div',{'class':'ui_qtext_expanded'}):
				print('\n')
				print('**************************ANSWER************************************')
				#file.write('\n')
				#file.write('*A*')
				#file.write('\n')
				#print(answer.prettify())
				print(cleanhtml(answer.get_text()))
				txtAnswer+=cleanhtml(answer.get_text())
				#file.write(cleanhtml(answer.get_text()))
			file.write('\"'+txtAnswer+'\"')
			file.write('\n')
		else:
			break
	file.close()
	

def cleanhtml(raw_html):
  cleanr = re.compile('<.*?>')
  cleantext = re.sub(cleanr, '', raw_html)
  cleanr = re.compile('"')
  cleantext = re.sub(cleanr, '', raw_html)
  #cleantext.replace('"', '\'')
  return cleantext

topic=input("Enter Quora topics:  ")
crawl_quora_topics(topic)