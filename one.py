#!/ usr/bin/env python 
#-*-coding=utf-8-*-
'''
获取一个app内容并推送到Kinlde，目前只能推送最新的一期，每天推送一次。
'''

import sys, re, requests, time
from bs4 import BeautifulSoup

reload(sys)
sys.setdefaultencoding( "utf-8" )
start = time.time()

#获取最新一期地址
one_url = 'http://wufazhuce.com/one'
r_one = requests.get(one_url)
soup_one = BeautifulSoup(r_one.text,'lxml')
url = soup_one.find('div',{'class':'corriente'}).a['href']


#处理最新章节
def new_index():
	r = requests.get(url)
	soup = BeautifulSoup(r.text,'lxml')
	soup.prettify()
#排版 去除空格
	pattern = re.compile(r'\t')

#写到文件
	f = open('one_new.txt','a+')
	f.write('第' + str(new_num) + '篇' + '\r')
	f.write(re.sub(pattern,'',soup.find('div',{'class':'comilla-cerrar'}).text) + "\n")
	f.write(re.sub(pattern,'',soup.find('h2',{'class':'articulo-titulo'}).text) + "\r")
	f.write("------" + re.sub(pattern,'',soup.find('p',{'class':'articulo-autor'}).text) + "\n")

#正文 处理去掉多余的字符
	soupcontent = soup.find('div',{'class':'articulo-contenido'})
	f.write(re.sub(r'\<.+\>','',soupcontent.text))
	f.close()

def previous_index():
	num = url.split('.')[2]
	i = 0
	f = open('one_10.txt','a+')
	while (i<10):
		url_previous = 'http://wufazhuce.com/one/vol.' + str(num) + '#articulo'
#		print url_previous
		r = requests.get(url_previous)
		soup = BeautifulSoup(r.text,'lxml')
		soup.prettify()
#排版 去除空格
		pattern = re.compile(r'\t')
#写到文件
		f.write('第' + str(num) + '篇' + '\r')
		f.write(re.sub(pattern,'',soup.find('div',{'class':'comilla-cerrar'}).text) + "\n")
		f.write(re.sub(pattern,'',soup.find('h2',{'class':'articulo-titulo'}).text) + "\r")
		f.write("------" + re.sub(pattern,'',soup.find('p',{'class':'articulo-autor'}).text) + "\n")
#正文 处理去掉多余的字符
		soupcontent = soup.find('div',{'class':'articulo-contenido'})
		f.write(re.sub(r'\<.+\>','',soupcontent.text) + "\n\n")
		num = int(num) - 1
		i = i + 1
	f.close()
if __name__ == '__main__':
	script, index = sys.argv
	index.decode('utf-8')
	new_num = url.split('.')[2]
	pre_num = int(new_num) - 10
	if index == '0':
		print "获取最新章节: " + new_num
		new_index()
	elif index == '10':
		print "获取最近10章： " + str(pre_num) + "-" + str(pre_num)
		previous_index()
	else:
		print "输入有误：请输入 0 or 10！"


end = time.time()
print "抓取时间： %.2f秒" %float(end-start)

