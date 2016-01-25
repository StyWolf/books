#!/ usr/bin/env python 
#-*-coding=utf-8-*-

import sys,re,textwrap
reload(sys)
sys.setdefaultencoding( "utf-8" )

dict ={u'零':0,u'一':1,u'二':2,u'两':2,u'三':3,u'四':4,u'五':5,u'六':6,u'七':7,u'八':8,u'九':9,u'十':10,u'百':100,u'千':1000,u'万':10000,u'亿':100000000}

#万以下基础转换
def zhconvertnum(chr):
	tmp = []
	count = 0
	while count < len(chr):
		num = chr[count:count+1]
		tmp.append(dict[num])
		count = count + 1

	i = 0 
	m = 0
	#处理‘零’
	if 0 in tmp:
		tmp.remove(0)
	else:
		pass

	if len(tmp) > 1 and len(tmp)%2 == 0:
		while i < len(tmp) - 1:
			n = tmp[i]*tmp[i+1]
			y = m + n 
			m = y 
			i = i + 2
	#处理个位数
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


#亿以下转换
def zhtonumwan(wan):
	if re.findall(u'万',wan) and wan.index(u'万') >= 2 :
		index = wan.index(u'万')
		wandown = wan[index+1:]
		wanup = wan[:index]
		num =  zhconvertnum(wanup) * 10000 + zhconvertnum(wandown)
		return num
	else:
		num  = zhconvertnum(wan)
		return num

#千亿以下转换
def zhtonum(string):
	if re.findall(u'亿',string) and string.index(u'亿') >= 1 :
		index = string.index(u'亿')
		yidown = string[index+1:]
		yiup = string[:index]
		wan = zhtonumwan(yidown)
		num =  zhconvertnum(yiup) * 100000000 + wan
		return ",".join(textwrap.wrap(str(num),3))
	else:
		num  = zhtonumwan(string)
		return ",".join(textwrap.wrap(str(num),3))












'''
a = u'两亿零五千六百万两千零三百六十二万零三百'
b = u'五十二万三千八百'
c = u'三百四十八万四千'
print zhtonum(a)

#print a.index(u'万')
'''

'''
#findall
p = ur'([两一二三四五六七八九十百千万]+)'
a = u'第三十九章 塞外 章'
s = re.findall(p,a)
print s[0]
b = zhconvertnum(s[0])
print b
'''
'''
a = u'第十万两千零十章 饿鬼王华丽的转身！'
#断言
req = re.compile(ur'(?<=第)[零两一二三四五六七八九十百千万]+(?=章)')
c =  req.findall(a)[0]

print zhconvertnum(c)
'''