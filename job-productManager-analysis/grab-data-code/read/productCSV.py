# coding=utf-8

import grabPageNumber as m
from bs4 import BeautifulSoup
import urllib2
import lxml
import csv
import time

import sys
reload(sys)
sys.setdefaultencoding('utf8')


# 产品经理链接
product_job_file = 'productJob.csv'

# 常量
fieldnames = ['salary', 'city', 'company', 'company_size', 'tag', 'work_experience', 'company_address', 'job_description', 'education', 'age', 'job_title']


# 读取数据
def readAll(page_list_file):

    page_dict_item = {}
    with open(page_list_file, 'wb') as f:
        w = csv.DictWriter(f, fieldnames)
        w.writeheader()

    for i in range(120):
        sourceFile = '../productPage/'+ str(i+1) +'.html'
        print sourceFile
        soup = BeautifulSoup(open(sourceFile),'lxml')
        m.job_page(soup, page_dict_item, fieldnames, page_list_file)


# 读取产品经理数据
readAll(product_job_file)