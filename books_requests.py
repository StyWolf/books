#!/usr/bin/env python
#-*-coding=utf-8-*-
import requests, sys, re, time, ConfigParser, zhtonum, os.path,hashlib
from bs4 import BeautifulSoup
from multiprocessing import Pool
from multiprocessing.dummy import Pool as ThreadPool



reload(sys)
sys.setdefaultencoding('utf-8')
# Python modules requests
# 之前一直用urllib2，看了requests的介绍，感叹urllib2真的难用了呀。
# 主要参考官方文档：http://cn.python-requests.org/zh_CN/latest/

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
	headers = {
                'User-Agent' : 'Mozilla/5.0 (Windows NT 6.0; WOW64; rv:24.0) Gecko/20100101 Firefox/24.0' ,
                'Connection' : 'keep-alive',
                'Accept'         : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Encoding' : 'gzip, deflate, sdch',
                'Accept-Language' : 'zh-CN,zh;q=0.8'
        }
	resp = requests.post(login_url,params=data,headers=headers)
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

#	print "BookName: ", soup_bookname.h1.text
#	print "BookAuthor: ", soup_bookname.p.text.decode("utf-8")

	for index in soup_bookname.find_all('a',href=re.compile('html')):
		urlhtml =  bookname_url + index['href']
		index_names.append(index.string)
		bookindexs.append(urlhtml)

#抓取全部内容，抓取的慢 1000章以上出现断线
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
	headers = {
		'User-Agent' : 'Mozilla/5.0 (Windows NT 6.0; WOW64; rv:24.0) Gecko/20100101 Firefox/24.0' ,
		'Connection' : 'keep-alive',
		'Accept'	 : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
		'Accept-Encoding' : 'gzip, deflate, sdch',
		'Accept-Language' : 'zh-CN,zh;q=0.8'
	}
	return requests.get(url,cookies=cookies,headers=headers)

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

#抓取新章节
def content_new():

	f = open(bookname + '.txt','a+')
	contents = rg(new_url)
	contents.encoding = 'gbk'
	soup_content = BeautifulSoup(contents.text,"lxml")

	soup_content.prettify()
	contents_books = index_name + "\n" +  re.sub(r'readx\(\)\;', '', soup_content.find('div',{'id':'content'}).text + '\n')
	f.write(contents_books + "\n")
	f.close()
	


def catch():
	config = ConfigParser.ConfigParser()
	with open('cfg.ini','r+') as cfgfile:
		config.readfp(cfgfile)
		section = config.options('info')

	for option in section:
		email =  config.get('info', option).split(',')[0]
		global bookname
		
		bookname = option.decode('utf-8')
		index()
		
		#n = re.search(r'\d+', str(index_names[0])).group(0)
		#print n
		index_L = re.search(r'\d+', str(index_names[0]))
		#print index_L
		if index_L != None:
			n = re.search(r'\d+', str(index_names[0])).group(0)
		
		else:
			pattern = re.compile(ur'(?<=^第)[零两一二三四五六七八九十百千万]+(?=章)')
			s = pattern.findall(index_names[0])
			n = zhtonum.zhtonum(s[0])
		

		if int(n) == int(config.get('info', option).split(',')[1]) and os.path.exists(bookname + '.txt'):
			'''
			# config.remove_option('hash', option)
			with open(bookname+ '.txt','rb') as f:
				md5 = hashlib.md5()
				md5.update(f.read())
				hashmd5 =  md5.hexdigest()
				print hashmd5
			config.set('hash', bookname,hashmd5)
			config.write(open('cfg.ini','w'))
			'''
			pass
			#new_url = bookindexs[0]
			#index_name = index_names[0]
			#content_new()
		else:
			i = int(n) - int(config.get('info', option).split(',')[1])
			m = i + 1 
			p = m 
			for url in bookindexs[-m:]:
				global new_url
				global index_name
				new_url = url
				index_name = index_names[-p]
				content_new()
				p = p - 1
#				time.sleep(3)
			
			config.set('info', option, email + ',' + str(n))
			config.remove_option('hash', option)
			config.write(open('cfg.ini','w'))
				#计算md5
			with open(bookname+ '.txt','rb') as f:
				md5 = hashlib.md5()
				md5.update(f.read())
				hashmd5 =  md5.hexdigest()
				# print hashmd5
			config.set('hash', bookname,hashmd5)
			config.write(open('cfg.ini','w'))
		bookindexs[:] = []
		index_names[:] = []

'''
if __name__ == '__main__':
	start = time.time()
	catch()
	end = time.time()
	print "抓取用时：%.2fs" %(end-start)
'''
