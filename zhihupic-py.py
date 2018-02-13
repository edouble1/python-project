'''
Copyright 2018 Edouble Zhang
Version 1.0
'''
import os
from urllib.request import urlretrieve
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
from selenium import webdriver
from selenium.webdriver import ActionChains
import time


def signin():
    print("是否登录？")
    print("1.是         2.否")
    if input()=='1':
        driver=webdriver.Chrome()                #用chrome浏览器打开
        driver.get("https://www.zhihu.com/")       #打开知乎我们要登录
        time.sleep(5)                            #让操作稍微停一下
        driver.find_element_by_link_text("登录").click() #找到‘登录’按钮并点击
        time.sleep(2)
        Account= input("输入帐号")                              
        driver.find_element_by_name('account').send_keys(Account) 
        time.sleep(2)
        Password=input("输入密码")
        driver.find_element_by_name('password').send_keys(Password)
        time.sleep(2)
        #输入浏览器中显示的验证码，这里如果知乎让你找烦人的倒立汉字，手动登录一下，再停止程序，退出#浏览器，然后重新启动程序，直到让你输入验证码
        #yanzhengma=input('验证码:')
        #driver.find_element_by_name('captcha').send_keys(yanzhengma)
        #找到登录按钮，并点击
        driver.find_element_by_css_selector('div.button-wrapper.command > button').click()

def website():#获取要抓取的网站
    website=input("输入要抓取的知乎回答网址：")#可加入判断条件
    if website!=None:
        return website
    else:
        print("未输入")
        website()

def imgnum():#定义要下载的图片数量
    print("需要下载多少图片？")
    imgnum=input()
    if imgnum=="all":
        return None
    else:
        return int(imgnum)

def dlplace():#定义下载地址
    print("下载到何处？")
    choose=(input("1. 默认    2.自定义"))
    if choose=='1':
        return None
    else:
        place=input()
    return place

def email():#输入邮箱，以便完成后邮件提醒
    print("发送邮件功能尚未实现")
    return email

def collect(website,images):#获取要下载的url
    for i in range(3):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(5)
    acs=driver.find_elements_by_xpath("//figure")
    NUM=1
    for ac in acs:
        ActionChains(driver).move_to_element(ac).perform()
        html=driver.page_source
        bs0bj=BeautifulSoup(html,'lxml')
        images.extend(bs0bj.findAll("img",{"src":re.compile("[https://]+[-A-Za-z0-9+&@#/%?=~_|!:,.;]+_hd\.jpg")}))
        acs=driver.find_elements_by_xpath("//figure")
        print("正在查看第%d张图"%NUM)
        NUM+=1
        time.sleep(2)
    return images

def name(bs0bj):#获取文件名
    webtitle=bs0bj.find("title").get_text()
    return webtitle

def down_load(news_pics,place,title):#下载图片
    num=1
    if place==None:
        place=title
    try:
        if not os.path.exists(place):
            print ('文件夹',place,'不存在，重新建立')
            #os.mkdir(file_path)
            os.makedirs(place)
        for pic in news_pics:
            print("正在下载第%d张图片……"%num)
            filename=('{}{}{}{}{}'.format(place,os.sep,title,num,'.jpg'))
            urlretrieve(pic,filename=filename)
            num+=1
        print("下载完成0w0")
    except IOError as e:
        print ('文件操作失败',e)
    except Exception as e:
        print ('错误 ：',e)
    
def send(email):#完成后发送邮件
    pass

#signin()
website=website()
# imgnum=imgnum()
place=dlplace()
# email=email()

driver=webdriver.PhantomJS(executable_path=r"D:\phantomjs-2.1.1-windows\bin\phantomjs.exe")
# driver=webdriver.Chrome()#chrome浏览器用于测试

driver.get(website)
time.sleep(3)
html=driver.page_source
bs0bj=BeautifulSoup(html,'lxml')
webname=name(bs0bj)
images=[]
urls=collect(website,images)
pics=[]
for image in images:
    pics.append(image["src"])
news_pics=[]
for pic in pics:
    if pic not in news_pics:
        news_pics.append(pic)
down_load(news_pics,place,webname)
send(email)