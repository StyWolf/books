#!/usr/bin/env python
#-*-coding=utf-8-*-

import sys, urllib, urllib2,cookielib

login_url = 'http://www.biquge.la/login.php?do=submit&action=login&usecookie=1&jumpurl='

data = {
		'username' : 'bookspush',
		'password' : 'zh123456'
	}
dataencode = urllib.urlencode(data)

def login():
	cookie = cookielib.CookieJar()
	handler = urllib2.HTTPCookieProcessor(cookie)
	opener = urllib2.build_opener(handler)
	resp = opener.open(login_url,dataencode)
	return opener
def testindex():
	#login()
	index = opener.open('http://www.biquge.la/message.php?box=inbox')
	print index.read()
#
#if __name__ == '__main__':
#	#user = 'bookspush'
#	#passwd = 'zh123456'
#	opener = login()
#	testindex()