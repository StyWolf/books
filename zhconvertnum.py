#!/ usr/bin/env python 
#-*-coding=utf-8-*-

import sys,re
reload(sys)
sys.setdefaultencoding( "utf-8" )

dict ={u'零':0,u'一':1,u'二':2,u'三':3,u'四':4,u'五':5,u'六':6,u'七':7,u'八':8,u'九':9,u'十':10,u'百':100,u'千':1000,u'万':10000,u'亿':100000000}
def zhconvertnum(string):
	tmp = []
	count = 0
	while count < len(string):
		num = string[count:count+1]
		tmp.append(dict[num])
		count = count + 1

	i = 0 
	m = 0
	if len(tmp) > 1 and len(tmp)%2 == 0:
		while i < len(tmp) - 1:
			n = tmp[i]*tmp[i+1]
			y = m + n 
			m = y 
			i = i + 2
	elif len(tmp) > 1 and len(tmp)%2 == 1:
		while i < len(tmp) - 1:
			n = tmp[i]*tmp[i+1]
			y = m + n 
			m = y 
			i = i + 2
		y = y + tmp[-1]
	else:
		y = tmp[0]

	return y

'''
#findall
p = ur'([一二三四五六七八九十百千万]+)'
a = u'第三十九章 塞外 章'
s = re.findall(p,a)
print s[0]
b = zhconvertnum(s[0])
print b
'''
a = u'第十卷 我看沧海化桑田 第一千九百五十章 龙皇变！'
#断言
req = re.compile(ur'(?<=第)[一二三四五六七八九十百千万]+(?=章)')
c =  req.findall(a)[0]
print zhconvertnum(c)
