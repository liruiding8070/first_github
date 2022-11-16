import requests
import threading
import pandas as pd
from lxml import etree

# 全部信息列表
count = list()



def url_creat():
    # 基础url
    url = 'https://qd.lianjia.com/ershoufang/pg{}/'
    links = [url.format(i) for i in range(1, 11)]
    return links


# 对url进行解析
def url_parse(url):
    headers = {
        'accept': 'image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9',
        'cache-control': 'no-cache',
        'pragma': 'no-cache',
        'referer': 'https://s1.ljcdn.com/matrix_pc/dist/pc/src/common/css/common.css?_v=20221031164757803',
        'sec-ch-ua': '"Google Chrome";v="107", "Chromium";v="107", "Not=A?Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'image',
        'sec-fetch-mode': 'no-cors',
        'sec-fetch-site': 'cross-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'
    }
    response = requests.get(url = url, headers = headers).text
    tree = etree.HTML(response)
    # ul列表下的全部li标签
    li_List = tree.xpath("//*[@class='sellListContent']/li")

    lock = threading.RLock()
    # 上锁
    lock.acquire()
    for li in li_List:
        # 标题
        title = li.xpath('./div/div/a/text()')[0]
        # 网址
        link = li.xpath('./div/div/a/@href')[0]
        # 位置
        postion = li.xpath('./div/div[2]/div/a/text()')[0] + li.xpath('./div/div[2]/div/a[2]/text()')[0]
        # 类型
        types = li.xpath('./div/div[3]/div/text()')[0].split(' | ')[0]
        # 面积
        area = li.xpath('./div/div[3]/div/text()')[0].split(' | ')[1]
        # 房屋信息
        info = li.xpath('./div/div[3]/div/text()')[0].split(' | ')[2:-1]
        info = ''.join(info)
        # 总价
        count_price = li.xpath('.//div/div[6]/div/span/text()')[0] + '万'
        # 单价
        angle_price = li.xpath('.//div/div[6]/div[2]/span/text()')[0]
        dic = {'标题': title, "位置": postion, '房屋类型': types, '面积': area, "单价": angle_price,
               '总价': count_price, '介绍': info, "网址": link}
        print(dic)
        # 将房屋信息加入总列表中
        count.append(dic)
    # 解锁
    lock.release()


# def init_db(dbpath):
#     sql = '''
#         create table homes
#         (
#         id integer primary key autoincrement,
#         title text,
#         link text,
#         postion text,
#         types text,
#         area text,
#         info text,
#         count_price text,
#         angle_price text
#         )
#     '''    #创建数据表
#     conn = sqlite3.connect(dbpath)
#     cursor = conn.cursor()
#     cursor.execute(sql)
#     conn.commit()
#     conn.close()


# def saveData2DB(datalist, dbpath):
#     init_db(dbpath)
#     conn = sqlite3.connect(dbpath)  # 链接数据库
#     cur = conn.cursor()  # 游标
#     for data in datalist:
#         for index in range(len(data)):
#             if index == 3 or index == 7 or index == 13:  # 遇见numeric类型时不转换成"xx"型
#                 continue
#             data[index] = '"' + data[index] + '"'  # 转换成"xx"型
#         sql = '''
#                 insert into homes (
#                 info_link,place,xiaoqu,size,chaoxiang,huxing,type,num,subway,decoration,key,new,time,money)
#                 values(%s)''' % ",".join(data)
#         cur.execute(sql)  # 执行sql语句
#         conn.commit()  # 提交结果
#     cur.close()  # 关闭游标
#     conn.close()  # 关闭连接
#
#     print("save....")

def run():
    links = url_creat()

    for i in links:
        x = threading.Thread(target = url_parse, args = (i,))
        x.start()
    x.join()
    # 将全部房屋信息转化为excel
    data = pd.DataFrame(count)
    data.to_excel('房屋信息.xlsx', index = False)


if __name__ == '__main__':
    run()
