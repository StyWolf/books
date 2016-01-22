# Books
###Books catch and push kindle or email.
1、添加模拟登陆网站，抓取不会出现1000多章错误
2 抓取一个app文章





**邮件乱码处理**
首先要确定那部分乱码和默认的编码，目前绝大多数都是支持utf-8编码的

1 处理附件中文内容
`#指定编码为utf-8`      
'''
att= MIMEText(f.read(),'base64','utf-8'])
'''
2 处理邮件中文标题 subject   
`#用email.header中的Header函数`     
'''
from email.header import Header

msg['subject'] = Header('subject','utf-8')
'''     

3 处理附件中文标题乱码    
`用email.header中的Header函数,返回的是instance需要转换成string拼接`  
'''
from email.header import Header    
att["Content-Disposition"] = 'attachment; filename=' + str(Header('subject','utf-8'))
'''