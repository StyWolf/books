#!/ usr/bin/env python 
#-*-coding=utf-8-*-
'''
smtp发送邮件
'''
import smtplib,sys
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


reload(sys)
sys.setdefaultencoding( "utf-8" )


postdata = {
	'from' 		: 'bookspush@163.com',
	'to'   		: 'senlief@163.com',
	'subject' 	: 'one',
	'fn_path'	: '.',
	'fn'		: ['一个_9.txt','一个_10.txt'],
	'encode'	: 'utf-8',
	'server'	: 'smtp.163.com',
	'port'		: '',
	'filename'	: ['one_9.txt','one_10.txt']	
}

def sendmail(username,password,data):
	msg = MIMEMultipart()
	for i in data['fn']:
		f = open(i.decode(),'rb')
		att= MIMEText(f.read(),'base64',data['encode'])
		att["Content-Type"] = 'application/octet-stream'
		att["Content-Disposition"] = 'attachment; filename=' + i.decode().encode('gbk')
		msg.attach(att)
		

	msg['to'] = data['to']
	msg['from'] = data['from']
	msg['subject'] = data['subject']

	try:
		server = smtplib.SMTP()
		server.connect(data['server'])
		server.login(username,password)
		server.sendmail(msg['from'],msg['to'],msg.as_string())
		server.quit()
		print '发送成功!'
	except Exception, e:
		print str(e)

sendmail('bookspush@163.com', 'zh123456',postdata)