# coding=utf-8
from bs4 import BeautifulSoup
import urllib2
import lxml
import csv
import time


# 读取链接内容
def readUrl(url):

    # 读取网页内容
    response = urllib2.urlopen(url)
    time.sleep(10)
    page_source = response.read()
    time.sleep(10)
    soup = BeautifulSoup(page_source, 'lxml')

    # 返回页面内容
    return soup

# 读取落地页内容，并写入csv文件
def job_page(soup_tmp, dict, fieldnames, pageData):

    dict['job_title'] = soup_tmp.find('div','title-info').find('h1')['title']
    dict['company'] = soup_tmp.find('div','title-info').find('a')['title']
    dict['salary'] = soup_tmp.find('p','job-item-title').text.split('\n')[0]
    dict['city'] = soup_tmp.find('p','basic-infor').find('span').text
    tmp = soup_tmp.find('div','job-qualifications').find_all('span')
    print tmp
    dict['education'] = tmp[0].text
    dict['work_experience'] = tmp[1].text
    dict['age']= tmp[3].text
    company_tmp = soup_tmp.find('ul', 'new-compintro').find_all('li')
    if len(company_tmp) > 2:
        dict['company_size'] = company_tmp[1].text
        dict['company_address'] = company_tmp[2].text
    elif len(company_tmp) > 1:
        dict['company_size'] = company_tmp[1].text
        dict['company_address'] = None
    else:
        dict['company_size'] = None
        dict['company_address'] = None
    tag = soup_tmp.find('div','tag-list')
    if tag != None:
        tag = tag.find_all('span','tag')
        tag_list = []
        for i in range(len(tag)):
            a = tag[i].text
            tag_list.append(a)
        dict['tag'] = ','.join(tag_list)
    else:
        dict['tag'] = None

    dict['job_description']  = soup_tmp.find('div','content content-word').get_text('\n')

    with open(pageData, 'a') as f:
        w = csv.DictWriter(f, fieldnames)
        w.writerow(dict)

    return dict

# 读取list里面每一个职位信息的落地页
def readJobLink(soup, filename, dict, list):

    for item in soup.find_all("div", "job-info"):
        href = item.find('h3').find('a').get('href')
        dict['link'] = href
        writeToFile(dict,filename)
        list.append(href)

# 把落地页链接写到文件里面
def writeToFile(link, filename):
    with open(filename, 'a') as f:
        w = csv.DictWriter(f,['link'])
        w.writerow(link)

# 读取链接，并写入文件
def urlToFile(page_num, source_link, filename, dict, list):
    for i in range(page_num):
        url = source_link + str(i)
        soup = readUrl(url)
        readJobLink(soup, filename, dict, list)


