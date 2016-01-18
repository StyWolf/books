#!/ usr/bin/env python 
#-*-coding=utf-8-*-

import sys, urllib, urllib2, re, time
from bs4 import BeautifulSoup
import login
from multiprocessing import Pool
from multiprocessing.dummy import Pool as ThreadPool


#防止编码错误
reload(sys)
sys.setdefaultencoding( "utf-8" )


#抓取搜索地址：笔趣阁
book_url = 'http://so.biquge.la/cse/search'

script, bookname, bookstatus  = sys.argv
bookname = bookname.decode("GB18030")

#bookname = u"玄界之门"

#目录名
bookindexs = []
#目录地址
index_names = []

#搜索
#-未实现模糊搜索，不计划实现
def search(book_name):
	data = {
		's' : '7138806708853866527',
		'q' : book_name,
		'click' : '1',
		'nsid' : ''
	}

	encode_data = urllib.urlencode(data)
	search_url = book_url + "?" + encode_data
	
	req = urllib2.Request(search_url)
	resp = urllib2.urlopen(req)
	global contents
	contents = resp.read()
	

#目录
# 获取章节信息，可以用数组输出
# 未实现书籍基本信息的获取，例如简介
def index():	
	soup = BeautifulSoup(contents,"lxml")
	soup.prettify()
	#global book_index
	book_index={}
	for i in soup.select('.result-game-item-title-link'):
		url =  i.attrs['href']
		name = i.text
		books_name = re.sub(r'\s', '',name)
		book_index[books_name] = url
	
	#indexs
	index_url = book_index[bookname]
	req_index = urllib2.Request(index_url)
	resp_index = urllib2.urlopen(req_index)

	soup_index = BeautifulSoup(resp_index.read(),"lxml")
	soup_index.prettify()
	
	print "BookName: ", soup_index.h1.text
	print "BookAuthor: ", soup_index.p.text.decode("utf-8")

	
	for index in soup_index.find_all('a',href=re.compile('html')):
		urlhtml =  index_url + index['href']
		index_names.append(index.string)
		bookindexs.append(urlhtml)
	
#全部内容
# 到最新章节全部内容
#- 章节太多抓取1000章左右会出错，应该是封IP。计划尝试登陆后抓取和模拟头信息。
#- 计划多线程抓取章节内容
#- 计划用数据库缓存后写入文件
#- 章节内容目前无法格式化，比较乱。
'''
def content():
	i = 0
	f = open(bookname + '.txt','a+')
	del bookindexs[0]
	del index_names[0]
	for content_url in bookindexs:

		content_req = urllib2.Request(content_url)
		content_resp = opener.open(content_req)

		contents = content_resp.read()
		soup_content = BeautifulSoup(contents,"lxml")
		soup_content.prettify()
		
		contents_books = index_names[i] + "\n" +  re.sub(r'readx\(\)\;', '', soup_content.find('div',{'id':'content'}).text + '\n')
		i = i + 1
	
		f.write(contents_books + "\n")
	f.close()
'''
def thread_content():
	i = 0
	f = open(bookname + '.txt','a+')
	del bookindexs[0]
	del index_names[0]
	pool = ThreadPool(5)
	contents_resp = pool.map(opener.open, bookindexs)
	for bookcontent in contents_resp:
		contents = bookcontent.read()
		soup_content = BeautifulSoup(contents,"lxml")
		soup_content.prettify()
		
		contents_books = index_names[i] + "\n" +  re.sub(r'readx\(\)\;', '', soup_content.find('div',{'id':'content'}).text + '\n')
		i = i +1
		f.write(contents_books + "\n")
	f.close()

#最新章节
# 目前仅实现脚本执行时更新的最后一章
#- 计划实现抓取每天更新的内容，增量推送。
def content_new():
	content_new_req = urllib2.Request(bookindexs[0])
	content_new_resp = opener.open(content_new_req)
	contents = content_new_resp.read()
	soup_content = BeautifulSoup(contents,"lxml")
	soup_content.prettify()
	contents_books = index_names[0] + "\n" +  re.sub(r'readx\(\)\;', '', soup_content.find('div',{'id':'content'}).text + '\n')

	f = open(bookname + "_" + "最新章节" + '.txt','a+')
	f.write(contents_books + "\n")
	f.close()


if __name__ == '__main__':
	time.clock()
	print "开始抓取！"
	opener = login.login()
	search(bookname)
	index()

	if bookstatus == '0':
		print "正在抓取全部章节内容，请耐心等待！"
		#content()
		thread_content()
	elif bookstatus == '1':
		print "正在抓取最新章节，请耐心等待！"
		content_new()
	else:
		print "请选择抓取全本或者最新章节（0 or 1）!"
	
	print "结束抓取！"
	print "抓取耗时 %.2f s !" %(float(time.clock()))