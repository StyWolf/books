#!/ usr/bin/env python 
#-*-coding=utf-8-*-


import sys, booksmtp, books_requests, time, ConfigParser, os.path


reload(sys)
sys.setdefaultencoding( "utf-8" )


pushdata = {
	'from' 		: 'bookspush@163.com',
	'to'   		: 'senlief@163.com',
	'subject' 	: '',
	'fn_path'	: '.',
	'fn'		: '',
	'encode'	: 'utf-8',
	'server'	: 'smtp.163.com',
	'port'		: '',
	'filename'	: ''	
}

def pushconfig():
	config = ConfigParser.ConfigParser()
	with open('cfg.ini','r+') as cfgfile:
		config.readfp(cfgfile)
		section = config.options('info')

	for option in section:
		email =  config.get('info', option).split(',')[0]
		bookname = option.decode('utf-8')
		
		pushdata['to'] = email
		pushdata['subject'] = bookname + '.txt'
		pushdata['fn'] = bookname + '_最新章节.txt' 
		pushdata['filename'] = bookname + '.txt'
		booksmtp.sendmail(username, password, pushdata)
#		os.remove(bookname + "_" + "最新章节" + '.txt')
		#if config.get('server',bookname):
		#	pushdata['server'] = config.get('server',bookname)
		#else:
		#	pass
		#print type(pushdata['fn'])

if __name__ == '__main__':
	start = time.time()
	username = 'bookspush@163.com'
	password = 'zh123456'
	books_requests.catch()
	pushconfig()
	#print type(pushdata['fn'])
	end = time.time()
	print "抓取用时：%.2fs" %(end-start)








