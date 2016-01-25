#!/ usr/bin/env python 
#-*-coding=utf-8-*-


import sys

reload(sys)
sys.setdefaultencoding( "utf-8" )



rdict =  {0:u'零',1:u'一',2:u'二',3:u'三',4:u'四',5:u'五',6:u'六',7:u'七',8:u'八',9:u'九',10:u'十'}


listzh = ['',u'十',u'百',u'千',u'万']
listnum = []
list = []
listwan = []

def numtozhbase(basestr):
	#print len(basestr)
	if len(basestr) > 1 and len(basestr) < 5 and len(basestr)%2 == 0:
		n = 0
		for i in basestr[::-1]:
			listnum.append(rdict[int(i)])
			list.append(listnum[n] + listzh[n])
			n = n + 1
		return  ''.join(list[::-1])
	elif len(basestr) > 1 and len(basestr) < 5 and len(basestr)%2 == 1:
		n=0
		list.append(rdict[int(basestr[-1])])
		for i in basestr[-2::-1]:
			listnum.append(rdict[int(i)])
			list.append(listnum[n] + listzh[n+1])
			n = n + 1

		return  ''.join(list[::-1])
	else:
		return rdict[int(basestr)]

def numtozhwan(wan):
	if len(wan) > 4:
		wanup = wan[:-4]
		#print wanup
		wandown = wan[-4:]
		print type(wandown)
		wanup = numtozhbase(wanup)
		print wanup
		#wand = numtozhbase(wandown)
		#print "wand值为： "  + wand
		listwan.append(numtozhbase(wandown))
		# print listwan
		listwan.append(wanup + u'万')
		#print listwan
		zh = ''.join(listwan[::-1]) 
		return zh



print numtozhbase('3864')
print  numtozhwan('433864')
