#!/ usr/bin/env python 
#-*-coding=utf-8-*-


import sys, booksmtp, books_requests, time, ConfigParser, os.path, hashlib


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
		old_hashmd5 = config.get('hash',option)
		bookname = option.decode('utf-8')
		
		pushdata['to'] = email
		pushdata['subject'] = bookname + '.txt'
		pushdata['fn'] = bookname + '.txt' 
		pushdata['filename'] = bookname + '.txt'

	'''
		if books_requests.catch.old_hashmd5 == books_requests.catch.hashmd5:
			pass
			print option + '--->' + "已经是最新章节，无需推送"
		else:
			booksmtp.sendmail(username, password, pushdata)
			os.remove(bookname + '.txt')
			print optin + '--->' + "已经完成最新章节推送"
		#if config.get('server',bookname):
		#	pushdata['server'] = config.get('server',bookname)
		#else:
		#	pass
		#print type(pushdata['fn'])
'''
if __name__ == '__main__':
	start = time.time()
	username = 'bookspush@163.com'
	password = 'zh123456'
	books_requests.catch()
	pushconfig()
	#print type(pushdata['fn'])
	end = time.time()
	print "推送用时：%.2fs" %(end-start)








