import re
import urllib.request, urllib.error
from bs4 import BeautifulSoup
import urllib.request, urllib.error
import xlwt
import urllib.request
from lxml import etree
import pymysql

url = 'https://sh.lianjia.com/zufang'
headers = {
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 Edg/107.0.1418.35"
}
request = urllib.request.Request(url = url, headers = headers)
response = urllib.request.urlopen(request)
content = response.read().decode('utf-8')
# 解析网页源码，来获取我们想要的数据


tree = etree.HTML(content)
# 获取想要的数据 xpath返回值是列表类型数据
findlianjie = tree.xpath('//div[@class="content__list--item"]/div/p[@class="content__list--item--title"]/a/@href')
print(len(findlianjie))

# 区域
findplace1 = re.compile(
    r'<a href="/zufang/.*" target="_blank">(.*)</a>-<a href="/zufang/.* target="_blank">.*</a>-<a href="/zufang.*" target="_blank" title=".*">.*</a>')  # 创建正则表达式对象，表示规则（字符串的模式）

findplace2 = re.compile(
    r'<a href="/zufang/.*" target="_blank">.*</a>-<a href="/zufang/.* target="_blank">(.*)</a>-<a href="/zufang.*" target="_blank" title=".*">.*</a>')

findplace3 = re.compile(
    r'<a href="/zufang/.*" target="_blank">.*</a>-<a href="/zufang/.* target="_blank">.*</a>-<a href="/zufang.*" target="_blank" title=".*">(.*)</a>')
# 房子大小
finddaxiao = re.compile(r'<i>/</i>(.*)<i>/</i>.*<i>/</i>.*<span class="hide">', re.S)  # re.s让换行符包含在字符中
# 房子朝向
findfangxiang = re.compile(r'<i>/</i>.*<i>/</i>(.*)<i>/</i>.*<span class="hide">', re.S)
# 房子规格
findguige = re.compile(r'<i>/</i>.*<i>/</i>.*<i>/</i>(.*)<span class="hide">', re.S)
# 楼层类型
findleixing = re.compile(
    r'<p class="content__list--item--des">.*<i>/</i>(.*)</span>.*</p>.*<p class="content__list--item--bottom oneline">',
    re.S)
# 是否靠近地铁
findsubway = re.compile(r'<i class="content__item__tag--is_subway_house">(.*)</i>')
# 是否是精装
finddecoration = re.compile(r'<i class="content__item__tag--decoration">(.*)</i>')
# 是否可以随时看房
findkey = re.compile(r'<i class="content__item__tag--is_key">(.*)</i>')
# 是否是新上的
findnew = re.compile(r'<i class="content__item__tag--is_new">(.*)</i>')
# 维护时间
findtime = re.compile(r'<span class="content__list--item--time oneline">(.*)</span>')
# 平均租金
findmoney = re.compile(r'<span class="content__list--item-price"><em>(.*)</em>')


def askURL(url):
    head = {  # 模拟浏览器头部信息，向链家服务器发送消息
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36"
    }
    # 用户代理，表示告诉链家服务器，我们是什么类型的机器，浏览器（本质上是爬虫）
    request = urllib.request.Request(url, headers = head)
    html = ""
    try:
        response = urllib.request.urlopen(request)
        html = response.read().decode("utf-8")
        # print(html)    测试用的
    except urllib.error.URLError as e:
        if hasattr(e, "code"):
            print(e.code)
        if hasattr(e, "reason"):
            print(e.reason)
    return html


def getData(baseurl):  # 调用获取页面信息的函数
    datalist = []  # 分配暂存的空间
    j = 0
    for i in range(0, 1):
        url = baseurl + str(i)
        html = askURL(url)  # 保存获取到的网页源码
        # print(html)    #测试用的代码

        # 逐一解析数据（边获取边解析）
        soup = BeautifulSoup(html, "html.parser")  # html.parser是html的解析器
        for item in soup.find_all('div', class_ = "content__list--item"):  # 查找符合要求的字符串，形成列表
            # print(item) #测试：查看链家item全部信息
            data = []
            item = str(item)  # 转换成字符串，否则无法识别
            # 链家详情链接
            # https://sh.lianjia.com/zufang/pg3/#contentList

            lianjie1 = findlianjie[j]
            j = j + 1
            lianjie2 = "https://sh.lianjia.com/zufang"
            lianjie = lianjie2 + lianjie1
            data.append(lianjie)  # 添加链接

            place1 = re.findall(findplace1, item)[0]  # re库用来通过正则表达式查找指定的字符串
            place2 = re.findall(findplace2, item)[0]
            place3 = re.findall(findplace3, item)[0]
            place = place1 + '-' + place2
            data.append(place)  # 添加地址

            data.append(place3)  # 添加小区

            daxiao = re.findall(finddaxiao, item)[0]
            daxiao = daxiao.strip()
            data.append(daxiao.replace("㎡", ""))  # 添加房子大小(平米)并替换前后空格

            fangxiang = re.findall(findfangxiang, item)[0]
            data.append(fangxiang.replace(" ", ""))  # 添加房子朝向并替换空格

            guige = re.findall(findguige, item)[0]
            data.append(guige.replace(" ", ""))  # 添加房子户型并替换空格

            leixing1 = re.findall(findleixing, item)[0]
            leixing2 = leixing1.strip()  # 去掉前后空格
            leixing3 = leixing2.replace(" ", "")  # 将空格替换掉
            data.append(leixing3[0:3])  # 添加房子楼层类型并替换空格

            data.append(leixing3[4:8].replace("层）", ""))  # 添加房子层数并替换掉()

            subway = re.findall(findsubway, item)  # 可能写有靠近地铁
            if (len(subway)) != 0:
                subway = subway[0]
                data.append(subway)  # 添加近地铁
            else:
                data.append("不靠近地铁")  # 添加不靠近地铁

            decoration = re.findall(finddecoration, item)
            if len(decoration) != 0:
                decoration = decoration[0]
                data.append(decoration)  # 添加精装
            else:
                data.append("不是精装")  # 添加不是精装

            key = re.findall(findkey, item)
            if len(key) != 0:
                key = key[0]
                data.append(key)  # 添加随时看房
            else:
                data.append("不是随时看房")  # 添加不是随时看房

            new = re.findall(findnew, item)
            if len(new) != 0:
                new = new[0]
                data.append(new)  # 添加新上
            else:
                data.append("不是新上")  # 添加不是新上

            time = re.findall(findtime, item)[0]
            data.append(time)  # 添加维护时间

            money = re.findall(findmoney, item)[0]
            data.append(money)  # 添加平均租金（元/月）

            datalist.append(data)  # 将data中的数据放入datalist中
    return datalist
    # 保存数据  输入区域和户型，输出该区域和户型的平均租金


# 保存数据  输入区域和户型，输出该区域和户型的平均租金
def saveData(datalist, savepath):
    print("save...")
    book = xlwt.Workbook(encoding = "utf-8", style_compression = 0)  # 创建workbook对象
    sheet = book.add_sheet('链家租房信息', cell_overwrite_ok = True)  # 创建工作表
    col = (
        "链接", "区域", "小区", "面积", "房子朝向", "户型", "楼层类型", "楼层", "是否靠近地铁",
        "是否是精装", "是否可以随时看房", "是否是新上", "维护事件", "平均租金")
    for i in range(0, 14):
        sheet.write(0, i, col[i])  # 列名
    for i in range(0, 30):
        print("第%d条" % (i + 1))
        data = datalist[i]
        for j in range(0, 14):
            sheet.write(i + 1, j, data[j])  # 数据
    book.save(savepath)


def saveData2DB(datalist):
    conn = pymysql.connect(host = '127.0.0.1'
                           , user = 'root'
                           , passwd = 'Ding8070'
                           , port = 3306
                           , db = 'test'
                           , charset = 'utf8'
                           )  # 链接数据库

    cur = conn.cursor()  # 游标
    for data in datalist:
        for index in range(len(data)):
            if index == 3 or index == 7 or index == 13:  # 遇见numeric类型时不转换成"xx"型
                continue
            data[index] = '"' + data[index] + '"'  # 转换成"xx"型
        sql = '''
                insert into house (
                info_link,place,xiaoqu,size,chaoxiang,huxing,type,num,subway,decoration,anytime,new,time,money)
                values(%s)''' % ",".join(data)
        cur.execute(sql)  # 执行sql语句
        conn.commit()  # 提交结果
    cur.close()  # 关闭游标
    conn.close()  # 关闭连接

    print("save....")


if __name__ == "__main__":
    baseurl = "https://sh.lianjia.com/zufang/pg"
    datalist = getData(baseurl)
    print(datalist)
    saveData(datalist, '房源信息.xlsx')
    saveData2DB(datalist)
