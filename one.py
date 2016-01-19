#!/ usr/bin/env python 
#-*-coding=utf-8-*-

import sys, re, requests, time
from bs4 import BeautifulSoup

reload(sys)
sys.setdefaultencoding( "utf-8" )


url = 'http://wufazhuce.com/one/vol.1198#articulo'
start = time.time()
r = requests.get(url)
#print r.text

soup = BeautifulSoup(r.text,'lxml')
soup.prettify()
#print soup.find('div',{'class':'one-imagen-leyenda'}).text
#print soup.find('div',{'class':'one-cita'}).text
print soup.find('div',{'class':'comilla-cerrar'}).text
print soup.find('h2',{'class':'articulo-titulo'}).text
print soup.find('p',{'class':'articulo-autor'}).text
print soup.find('span',{'style':'line-height:1.6em'}).text
soupcontent =  soup.find_all('p')

print re.sub(r'[\<br\/\>\<p\>\<\/p\>]','',str(soupcontent[4]))
end = time.time()
print end-start


