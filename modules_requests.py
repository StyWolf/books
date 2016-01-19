#-*-coding=utf-8-*-
import requests, sys, re, time
from bs4 import BeautifulSoup
from multiprocessing import Pool
from multiprocessing.dummy import Pool as ThreadPool



reload(sys)
sys.setdefaultencoding('utf-8')
# Python modules requests
# 之前一直用urllib2，看了requests的介绍，感叹urllib2真的难用了呀。
# 主要参考官方文档：http://cn.python-requests.org/zh_CN/latest/
'''
#以下是官网给出的特性
功能特性

1、国际化域名和URLs
2、Keep-Alive & 连接池
3、持久的Cookie会话 
4、类浏览器式的SSL加密认证
5、基本/摘要式的身份认证
6、优雅的键/值Cookie
7、自动解压
8、Unicode编码的响应体
9、多段文件上传
10、连接超时
11、支持.netrc
12、适用于Python2.7和Python3.4
13、线程安全
'''


#目录名
bookindexs = []
#目录地址
index_names = []
#最近在练习爬虫 抓小说 就以笔趣阁为例吧

def login():
	login_url = 'http://www.biquge.la/login.php?do=submit&action=login'
	url = 'http://www.biquge.la/'
	data = {
		'username' : 'bookspush',
		'password' : 'zh123456',
		'jumpurl'   : url
	}
	resp = requests.post(login_url,params=data)
	resp.encoding = 'gbk'
#Cookies
	cookies = resp.cookies
	return cookies

#Search
def search(name):
	global cookies
	cookies = login()
	search_url = 'http://so.biquge.la/cse/search'
	payload = {
		's' : '7138806708853866527',
		'q' : name,
		'click' : '1',
		'nsid' : ''
	}
	resp = requests.get(search_url,params=payload,cookies=cookies)
	resp.encoding = 'utf8'
	contents = resp.text
	return contents

#index
def index():
	contents = search(bookname)
	soup = BeautifulSoup(contents,'lxml')
	soup.prettify()

	book_index={}
	for i in soup.select('.result-game-item-title-link'):
		url =  i.attrs['href']
		name = i.text
		books_name = re.sub(r'\s', '',name)
		book_index[books_name] = url

	#print book_index
	bookname_url = book_index[bookname]
	resp_bookname = requests.get(bookname_url,cookies=cookies)
	resp_bookname.encoding = 'gbk'
	soup_bookname = BeautifulSoup(resp_bookname.text,'lxml')
	soup_bookname.prettify()

	print "BookName: ", soup_bookname.h1.text
	print "BookAuthor: ", soup_bookname.p.text.decode("utf-8")

	for index in soup_bookname.find_all('a',href=re.compile('html')):
		urlhtml =  bookname_url + index['href']
		index_names.append(index.string)
		bookindexs.append(urlhtml)

def content():
	i = 0
	f = open(bookname + '.txt','a+')
	del bookindexs[0]
	del index_names[0]
	for content_url in bookindexs:
		contents = requests.get(content_url,cookies=cookies)
		contents.encoding = 'gbk'
		soup_content = BeautifulSoup(contents.text,"lxml")
		soup_content.prettify()
		
		contents_books = index_names[i] + "\n" +  re.sub(r'readx\(\)\;', '', soup_content.find('div',{'id':'content'}).text + '\n')
		i = i + 1
	
		f.write(contents_books + "\n")
	f.close()	

def rg(url):
	return requests.get(url,cookies=cookies)

#线程池
def thread_content():
	i = 0
	del bookindexs[0]
	del index_names[0]
#	print bookindexs
	pool = ThreadPool(5)
	contents_resp = pool.map(rg, bookindexs)
	pool.close()
	pool.join()
#	print type(contents_resp),contents_resp
	f = open(bookname + '.txt','a+')
	for bookcontent in contents_resp:
		bookcontent.encoding = 'gbk'
		contents = bookcontent.text
		soup_content = BeautifulSoup(contents,"lxml")
		soup_content.prettify()
		
		contents_books = index_names[i] + "\n" +  re.sub(r'readx\(\)\;', '', soup_content.find('div',{'id':'content'}).text + '\n')
		i = i +1
		f.write(contents_books + "\n")
	f.close()
	



if __name__ == '__main__':
	start = time.time()
	bookname = u'我欲封天'
	index()
	thread_content()
	#content()
	end = time.time()
	print end-start
