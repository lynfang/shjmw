import requests
import re
import json
import random
import lxml
from bs4 import BeautifulSoup
import pymongo

payload={}
headers = {
  'Cookie': '__yjs_duid=1_5c3464c1b5a03e57f3f454dae1704d0f1619073829953; 1r6v_2132_forum_lastvisit=D_98_1619073829; 1r6v_2132_lastact=1619073829%09forum.php%09forumdisplay; 1r6v_2132_lastvisit=1619070229; 1r6v_2132_pc_size_c=0; 1r6v_2132_saltkey=ibBD33K0; 1r6v_2132_sid=DV66H5; 1r6v_2132_st_t=0%7C1619073829%7Ce147964d55a431d969b7d429d16a5651; 1r6v_2132_visitedfid=98'
}

def request_page(url):
  try:
    response = requests.request("GET", url, headers=headers, data=payload)
    if response.status_code == 200:
      return response.text
  except requests.RequestException:
    return None

def parse_result(html):
  search_O = re.search('.*thread-(\d+)-.*',str(html),re.S)

  #print (search_O.group(1))
  items = search_O.group(1)
  #items = list(filter(pattern.match, html))
  return items

def parse_result2(html):
  ## 过滤html元素
  reg = re.compile('<[^>]*>')
  try:
    searchpage_result = reg.sub('',str(html))
  except AttributeError:
    searchpage_result = None

  return     searchpage_result


def get_data1(url,flaG):
  soup = BeautifulSoup(request_page(url), 'lxml')
  pageNum_dic = {}
  pageSub_tent = []
  pageCommmit = soup.find_all( id=True,class_="t_f")
  pageSub_tilte = soup.title.string
  ### 测试模式打印 子页面 评论的内容
  # if testMode < 5:
  #   for pageCommmitLine in pageCommmit:
  #     print (parse_result2(html=pageCommmitLine) )
  for pageCommmitLine in pageCommmit:
    pageSub_tent.append(parse_result2(html=pageCommmitLine))

  pageNum_dic[pageSub_tilte] = pageSub_tent
  return  pageNum_dic

def connMongo(title,url):
  conn = pymongo.MongoClient('mongodb://localhost:27017/')
  db = conn['beichao']
  mycol = db['title']
  db.mycol.insert({"title": title, 'url':url })



def get_data(url,flaG):

  pageNum = 0
  soup = BeautifulSoup(request_page(url), 'lxml')
  tizhi_info = []
  pageNum_dic = {}


  if flaG == 1 :
    for tag in soup.find_all('a', href=True):

      #url_line =  re.search("thread.*html",tag['href'])




      url_line = re.search('.*thread-(\d+)-.*', (tag['href']), re.S)
      if url_line:

        pageNum_dic[parse_result(url_line)]  = pageNum
       #page_num.append(parse_result(url_line))
    return pageNum_dic


def main():
  url = "http://www.sheitc.sh.gov.cn/zxgkxx/index.html"
  testMode_Flag = 40
  pageNum_dic = get_data(url,flaG=1)


  testFlag = 0
  for page_num in pageNum_dic.keys():
    testFlag = testFlag + 1
    detail_url = 'https://bbs.northdy.com/forum.php?mod=viewthread&tid=' + page_num
    #print  ("%s%s%s" % (detail_url,"\t\t",pageNum_dic[page_num]))
    subPage_con = get_data1(detail_url,flaG=2)
    if testMode_Flag < 5 :
      try:
        getdata_result = subPage_con
      except AttributeError:
        getdata_result = None
      print (getdata_result)

    else :
      getdata_result = subPage_con
      for page_title in getdata_result.keys():
        connMongo(page_title,detail_url)


        #write_item_to_file(page_title,getdata_result[page_title])



if __name__ == "__main__":
  main()