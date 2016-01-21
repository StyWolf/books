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


def sendmail(username,password,data):
	msg = MIMEMultipart()
#	for i in data['fn']:
	f = open(data['fn'].decode(),'rb')
	att= MIMEText(f.read(),'base64',data['encode'])
	att["Content-Type"] = 'application/octet-stream'
	att["Content-Disposition"] = 'attachment; filename=' + data['filename'].decode('utf-8')
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

#sendmail('bookspush@163.com', 'zh123456',postdata)