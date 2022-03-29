# -*- coding:utf-8 -*-

import random
import time
import requests
import xlwt

# 创建excell保存数据
file = xlwt.Workbook(encoding='utf-8')
sheet = file.add_sheet('data', cell_overwrite_ok=True)
for i in range(100):  # for循环遍历，批量爬取评论信息
        # 构造url，通过在网页不断点击下一页发现，url中只有page后数字随页数变化，批量遍历就是根据这个
        # url去掉了callback部分，因为这部分内没有有用数据，并且不去掉后面转换为json格式会有问题
    url = 'https://club.jd.com/comment/productPageComments.action?productId=3487483&score=0&sortType=5&page=%s&pageSize=10&isShadowSku=0&rid=0&fold=1' % i
    # 构造headers
    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36',
        'referer': 'https://item.jd.com/3487483.html',
    }
    response = requests.get(url, headers=headers).json()    # 字符串转换为json数据
    data = response["comments"] 
    print(data)
    print('正在爬取第%s页，url为：%s' %(i,url))    # print(data)
    page = (i * 10)+1 # 这里是存储在excell中用到的，因为每爬取一个url会有10条评论，占excell 10列
    if (data):
        col = ("用户ID", "评论内容", "手机型号")
        for a in range(0, 3):
            sheet.write(0, a, col[a])  # 列名
        for temp in data:
            sheet.write(page, 0, temp['id'])  # id
            sheet.write(page, 1, temp['content'])  # 评论
            sheet.write(page, 2, temp['referenceName']) # 手机型号
            page = page + 1
        print('第%s页爬取成功' % i)
    else:
        print('.............第%s页爬取失败' % i)
    file.save('JDComments耳机.xlsx')  # 保存到本地
    time.sleep(random.random() * 5)  # 每循环一次，随机时间暂停再爬

