#!/usr/bin/env python
# encoding: utf-8
"""
@author: zjl
@file: hero.py
@time: 2020/10/22 0022 22:37
"""
import requests
# import re
import time
from lxml import etree
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_argument('--headless')
driver = webdriver.Chrome('C:\\driver\\chromedriver.exe', chrome_options=chrome_options)
driver.maximize_window()
driver.get('https://pvp.qq.com/web201605/wallpaper.shtml')
hero_xpath = etree.HTML(driver.page_source)

# 逻辑获取页数
# page_search = re.compile(r'1/(\d+)')
# page_count = hero_xpath.xpath('//*[@id="Page_Container_267733"]/span[@class="totalpage"]/text()')[0]
# page = re.search(page_search, page_count).group(1)

# 循环判断是否还有翻页
for now_page in range(0, 23):
    try:
        wallpaper_xpath = hero_xpath.xpath('//*[@id="Work_List_Container_267733"]/div')
        for wallpaper_item in wallpaper_xpath:
            try:
                hero_name = wallpaper_item.xpath('./img/@alt')[0]
                if wallpaper_item.xpath('./ul/li[5]/a/span/text()')[0] == '1920x1080':
                    hero_img_url = wallpaper_item.xpath('./ul/li[5]/a/@href')[0]

                    # 得到图片路径后，需要再请求一次
                    header = {
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36'
                    }
                    response = requests.get(url=hero_img_url, headers=header)
                    with open('./wallpaper/' + hero_name + '.jpg', 'wb') as f:
                        f.write(response.content)
                    print('第' + str(now_page + 1) + '页' + '--->' + hero_name + '下载中......')
                    print('下载成功.......')
                    print('----------------------------------------')
            except Exception as e:
                print(e)
                continue

        # 点击下一页
        next_page = driver.find_element_by_xpath("./html/body/div[3]/div/div/div[2]/div[2]/div[3]/a[@class='downpage']")
        next_page.click()
        # 重新赋值
        hero_xpath = etree.HTML(driver.page_source)

        time.sleep(3)
    except Exception as e:
        print(e)
        continue

driver.close()