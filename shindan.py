# encoding=utf-8

import urllib
import sys
from HTMLParser import HTMLParser

class ShindanParser(HTMLParser):
  def __init__(self):
    HTMLParser.__init__(self)
    self.data = None
    self.inForm = False
    self.flag = False
  def handle_starttag(self,tagname,attribute):
    if tagname.lower() ==  'form':
      for attr in attribute:
       if attr == ('id','forcopy'):
          self.inForm = True
    elif tagname.lower() == 'textarea':
      if self.inForm:
        self.flag = True
  def handle_data(self,data):
    if self.flag:
      self.data = data
  def handle_endtag(self,tagname):
    if self.flag:
      self.flag = False
    if self.inForm and tagname.lower() == 'form':
      self.inForm = False

class Shindan:
  HOST = 'http://shindanmaker.com/'
  @classmethod
  def shindan(cls,id,name):
    if not id.isdigit(): return
    data = {'from':'','submit':'診断する'}
    data['u'] = name
    params = urllib.urlencode(data)
    url = Shindan.HOST + id
    res = urllib.urlopen(url, params)
    status = res.code
    if status != 200: return status,None
    parser = ShindanParser()
    parser.feed(res.read().decode('utf-8'))
    parser.close()
    return status, parser.data.encode('utf-8')

if __name__ == '__main__':
  argv = sys.argv
  argc = len(argv)
  if argc!=3:
    print "Usage: python %s SHINDAN_NO YOUR_NAME" % argv[0]
    quit()
  print "Shindan %s %s" % (argv[1],argv[2])
  st, cont = Shindan.shindan(argv[1],argv[2])
  print "Status code: %d , Result: %s" % (st, cont)
  
