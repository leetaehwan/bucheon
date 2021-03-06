import requests
from bs4 import BeautifulSoup
import re
import math


PAGE = 1
URL = f"http://reserv.bucheon.go.kr/site/main/lecture/lectureList?cp={PAGE}&pageSize=16&listType=list&viewMode=image"


def find_lastpage(n=1):
  PAGE = n
  URL = f"http://reserv.bucheon.go.kr/site/main/lecture/lectureList?cp={PAGE}&pageSize=16&listType=list&viewMode=image"
  result = requests.get(f"{URL}")

  soup = BeautifulSoup(result.text, "html.parser")

  total_left = soup.find("div","total left-fl")

  link = total_left.find("span")

  character = link.string

  characters = re.findall(r'\w', character)
  string = ""
  for i in range(len(characters)):
    if characters[i].isnumeric():
      string = string+characters[i]
  item_number = int(string)
  page_number = math.ceil(item_number/16)+1

  return page_number

def extract_lect(html):
  # try:
  #   title_raw = html.find_all('span','tit')
  #   title = [
  #     (i.contents[0]) for i in title_raw
  #   ]
  # except(TypeError):
  #   pass
  title_raw = html.find("span", {"class":"tit"})
  if title_raw.string is not None:
    title = title_raw.string
  else:
    print(title_raw)

  period_raw = html.find('div', {"class":'apl-time'})
  if period_raw.string is not None:
    period = period_raw.string
  else:
    print(period_raw)
  
  # url_raw = html.find_all('a')

  image_urls = html.img['alt']
  image = image_urls.string

  return {
    "title": title,
    "period": period,
    "image_url": image
    }
    # return {
    # "title": title,
    # "period": period,
    # # "image_url": image_urls
    # }
  
  
  

#   return title

#   return title
  # title_lists = soup.find_all('span','tit')
  # titles = []
  # for resul in title_lists:
  #   titles.append(resul.string)
  
  # period_lists = soup.find_all('div', 'apl-time')
  # periods = []
  # for resul in period_lists:
  #   periods.append(resul.string)

  # for result in soup:
  #   apply_link_lists = soup.find_all('a',string='/site/main/lecture/lectureInfoForm?lec_seq=')
  # apply_links = []
  # for resul in apply_link_lists:
  #   apply_links.append(resul.find['href'])

  # lectures = dict(zip(titles,periods))
  

def extract_BcLect_item(page_number):
  lects = []
  for page in range(1,page_number):
    print(f"Scrapping page {page}")
    URL = f"http://reserv.bucheon.go.kr/site/main/lecture/lectureList?cp={page}&pageSize=16&listType=list&viewMode=image"
    result = requests.get(f"{URL}")
    soup = BeautifulSoup(result.text, "html.parser")
    results = soup.find_all({'ul', 'li'}, class_=['li01','li02'])
    
    for result in results:
      if re.search('032-320-3000',result):
        lect = extract_lect(result)
        lects.append(lect)
    # for lect in lects:
    #   lects = extract_lect(lect)
      # title.append(lect.find_all('span','tit'))
  return lects