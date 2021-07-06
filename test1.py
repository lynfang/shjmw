import requests
import re
import json
import random
import lxml
from bs4 import BeautifulSoup
import pymongo


payload={}
headers = {
    'User-Agent'  :  'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36'
}

TAG_RE = re.compile(r'<[^>]+>')

def request_page(url):
  try:
    response = requests.request("GET", url, headers=headers, data=payload)
    if response.status_code == 200:
      return response.text
  except requests.RequestException:
    return None


def parse_result2(html):
  ## 过滤html元素
  reg = re.compile('<[^>]*>')
  try:
    searchpage_result = reg.sub('',str(html))
  except AttributeError:
    searchpage_result = None

  return     searchpage_result

def get_data(url):
    sub_pages = []


    soup = BeautifulSoup(request_page(url),'lxml')
    for tag in soup.find_all('a', href=True):
        if  re.search('.*2021.*', (tag['href']), re.S):
            #print (tag['href'])
            sub_pages.append(tag['href'])
    return  sub_pages



def get_data1(url):
    pagesub_dic = {}
    if request_page(url):
        soup = BeautifulSoup(request_page(url), 'lxml')
        pageSub_tent = []
        pageData = soup.find_all( class_="view_tit_1")
        pageSubContent= soup.find_all(id="ivs_content")
        pageSubContent = parse_result2(pageSubContent)

        #print    (pageSubContent)

        pageSub_tilte = soup.title.string
        if pageSubContent and pageSub_tilte :
            pagesub_dic[pageSub_tilte] = pageSubContent
    return  pagesub_dic



        #print (pageSub_tilte)
          ### 测试模式打印 子页面 评论的内容
          # if testMode < 5:
          #   for pageCommmitLine in pageCommmit:
          #     print (parse_result2(html=pageCommmitLine) )



def connMongo(title,content):
  conn = pymongo.MongoClient('mongodb://localhost:27017/')
  db = conn.sheitc

  db.mycol.insert({"title": title, 'content': content})


def main():
  url = "http://www.sheitc.sh.gov.cn/zxgkxx/index.html"
  testMode_Flag = 40
  sub_pages = get_data(url)

  for sub_page in sub_pages:
      sub_page = "http://www.sheitc.sh.gov.cn" + sub_page
      pagetext = get_data1(sub_page)

  for page_title in pagetext.keys():
      connMongo(page_title,pagetext[page_title] )





if __name__ == "__main__":
  main()