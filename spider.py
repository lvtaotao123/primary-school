import requests
from lxml import etree
import re
import numpy
import csv
import itertools

def get_html():#获取所有的年及
	arr = []
	html = requests.get("https://www.namibox.com/v/dictate/").text
	html1 = etree.HTML(html)
	par = '//a[@target="link"]/@href'
	url = html1.xpath(par)
	for i in url:
		url1 = "https://www.namibox.com"+str(i)
		arr.append(url1)
	return arr

def html2(list):#获取所有年纪的所有版本教材
	url = []
	for data in list:
		html1 = requests.get(data).text
		html = etree.HTML(html1)
		tag1 = data[-1]
		tag2 = data[-2]
		tag = tag2 + tag1
		
		par1 = '//a[@target="tape'+tag+'"]/@href'
		
		url3 = html.xpath(par1)
		
		
		for i in url3:
			url33 = "https://www.namibox.com"+i
			url.append(url33)
	return url


def get_text1(html): #获取所有教材的所有目录和，并保存在文件夹
	html_tree = etree.HTML(html)
	title_par = '//div[@class="toptitle"]/div[1]/text()'
	banben_par = '//div[@class="toptitle"]/div[2]/text()'
	comment_par = '//div[@class="v3inline_middle"]/text()'
	url_par = '//av[@targets="u_share"]/@hrefs'

	urlss = []
	title = html_tree.xpath(title_par)   # 几年级
	banben = html_tree.xpath(banben_par) #版本号
	#comment = html_tree.xpath(comment_par)  #章节  '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
	urls = html_tree.xpath(url_par)
	for u in urls:
		uu = "https://www.namibox.com"+u
		urlss.append(uu)
	mp3 = []
	pinyins = []
	word = []
	if len(banben) == 0:
		banben.append("沪教版")
	print("正在爬"+str(title[0])+str(banben[0]))
	path = "./小学语文/"+str(title[0])+str(banben[0])+".csv"
	comment_new =[]


	
	for url in urlss:
		html1 = requests.get(url).text
		if url == "https://www.namibox.com/dictation/do?url_content=tape1a/022002_语文（S版）/dictation&lesson=000029_看图说话学拼音_拼音10":
			break;
		mp3_name,pinyin,words,content,comment = get_text2(html1,url)
		



		for i in mp3_name:
			get_mp3(content,i)
			mp3.append(i)
		for j in pinyin:
			pinyins.append(j)
		for z in comment:
			comment_new.append(z)

		for num in range(0,len(mp3_name)):
			if num >=len(comment):
				comment_new.append(" ")
			title.append(" ")
			banben.append(" ")

		for nnn in words:
			word.append(nnn)

	with open(path,"w",newline='',encoding="gb2312") as f:
		writer=csv.writer(f)
		header=["年级","版本","课程","拼音","答案","语音"]
		writer.writerow(header)
		for i1 in itertools.zip_longest(title,banben,comment_new,pinyins,word,mp3,fillvalue=""):
			try:
				writer.writerow(i1)
			except :
				print(i1)

def get_text2(html,url1111):    #得到网页链接尾部，得到词语集合，拼音集合
	print(url1111)
	mp3_name = []     #mpe mingzi 
	words = []   #结果
	pinyin = []    #拼音
	dataf = []
	num = []
	com100 = []
	parse1 = 'var.*?list_words.*?=(.*?);'
	parse2 = 'var.*?list_lesson.*?= (.*?);'
	comment1 = re.compile(parse2,re.S).findall(html)
	comment = eval(comment1[1])
	c = list(comment.values())
	
	com100.append(c[0][1])
	#print(com100)
	comm = comment.values()
	name = re.compile(parse1,re.S).findall(html)
	data1 = eval(name[1])
	
	for i in data1:
		mp3_name.append(i[-1])
		num.append(len(i[2]))
		for j in i[2]:
			dataf.append(j)
	dataarr = numpy.array(dataf).T
	page1 = 0
	y = 0
	page = 0
	z = 0
	
	

	word_list = dataarr[0]
	pinyin_list = dataarr[1]
	for a in range(0,len(num)):
		page += num[a]
		word = ""
		for it in range(z,page):
			word += word_list[it]
		z = page	
		words.append(word)
	
	for a in range(0,len(num)):
		page1 += num[a]
		yin = ""
		for it in range(y,page1):
			yin += pinyin_list[it]
		y = page1	
		pinyin.append(yin)


	url_content_par = "url_content=(.*?)';"
	url_content = re.compile(url_content_par).findall(html)
	content = url_content[0].replace("&lesson=","/")+"/"
	
	
	return mp3_name,pinyin,words,content,com100	


def get_mp3(b,c):
	a = "https://ra.namibox.com/tina/static/d/"
	url = a+b+c
	path = "./小学语文/音频/"+c
	with open(path,"wb") as fh:
		content = requests.get(url).content
		fh.write(content)
		fh.close()





list1 = get_html()
list2 = html2(list1) #所有教材的链接

for aaa in list2:
	html = requests.get(aaa).text
	get_text1(html)
