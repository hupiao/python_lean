# -*- coding:utf-8 -*-
import sys
import requests
from bs4 import BeautifulSoup
import re
import xlwt
import time
from fake_useragent import FakeUserAgent

ua = FakeUserAgent()

reload(sys)
sys.setdefaultencoding('utf8')

list = ['glibc', 'Microsoft Office Word', 'Microsoft Internet Explorer']  # 想要查询的相关漏洞
num = []  # 存放每个实体对应的漏洞数目
page = []  # 存放每个实体对应的漏洞的页数


# 根据url爬取网页
def getHTMLTEXT(url, code="utf-8"):
    kv = {'user-agent': ua.random}  # 模拟浏览器访问网站 随机代理
    print kv
    try:
        # time.sleep(random.randrange(3, 5))
        r = requests.get(url, headers=kv, timeout=30)
        r.raise_for_status()
        r.encoding = code
        return r.text
    except:
        print 'not found url: %s' % url
        return ""


# 初始网页
def parsepage(name, url):
    html = getHTMLTEXT(url)
    soup = BeautifulSoup(html, 'html.parser')
    # 每个类型的数量
    # text=soup.find_all('a',text=re.compile('总条数：'))
    # num.append(re.findall(r'[0-9,]+',text.__str__()[:][:]))
    # 统计当前实体搜索结果共有多少页
    value = soup.find_all('input', id="pagecount")
    numcount = soup.find_all('a', onmouse="")
    print u"count is %s..............." % str(numcount[0].string)
    page.append(re.findall(r'[0-9]+', value.__str__()))
    print page


def get_ldjj(des):
    des = ''.join([i.encode('utf-8').strip() for i in des])
    des = BeautifulSoup(des, 'html.parser')
    ldjj = des.find_all('p', style="text-indent:2em")
    ldjj_1 = des.find_all('p', style="text-indent:2em;width: 890px;")
    ldjj.extend(ldjj_1)
    tmp_str = u''.join([str(jj.string).strip() for jj in ldjj if jj.string and str(jj.string).strip()])
    if not tmp_str:
        tmp_str = u''
    return tmp_str


def get_cvss(cve_id):
    html = getHTMLTEXT('http://cve.scap.org.cn/vuln/VH-' + cve_id)
    soup = BeautifulSoup(html, 'html.parser')
    # 寻找cvss
    # vul_grade = soup.find_all('div', attrs={'class': 'fl vul_grade'})
    #
    # des = ''.join([i.encode('utf-8').strip() for i in vul_grade[0]])
    # des = BeautifulSoup(des, 'html.parser')
    cvss_value = u''
    usability_value = u''
    if soup:
        cvss = soup.find_all('span', attrs={'data-toggle': "tooltip", 'data-placement': "bottom"})
        if cvss:
            cvss_value = str(cvss[0].string).strip().encode('utf-8')
            cvss_value = u'' if cvss_value == '-' else cvss_value

            usability = cvss[6]['title'].split(':')
            if len(usability) > 1:
                usability_value = u'{}'.format(str(usability[1]).strip())
    return cvss_value, usability_value


def init_xls():
    # 将列表信息写入EXCEL中
    f = xlwt.Workbook()  # 创建EXCEL工作簿
    sheet1 = f.add_sheet(u'sheet1', cell_overwrite_ok=True)  # 创建sheet
    sheet1.write(0, 0, u"漏洞名称")
    sheet1.write(0, 1, u"CNNVD编号")
    sheet1.write(0, 2, u"危害等级")
    sheet1.write(0, 3, u"漏洞类型")
    sheet1.write(0, 4, u"发布时间")
    sheet1.write(0, 5, u"威胁类型")
    sheet1.write(0, 6, u"更新时间")
    sheet1.write(0, 7, u"CVE编号")
    sheet1.write(0, 8, u"漏洞简介")
    sheet1.write(0, 9, u"漏洞公告")
    sheet1.write(0, 10, u"参考")
    sheet1.write(0, 11, u"受影响实体")
    sheet1.write(0, 12, u"解决方案")
    sheet1.write(0, 13, u"CVSS")
    sheet1.write(0, 14, u"可利用性")
    return f, sheet1


# 爬取对应漏洞下所有的网页
def save_xls(index, link, f, sheet1, qstartdate, qenddate):
    cnnvd_id = []  # CNNVD 编号
    level = []  # 漏洞危害等级
    cve_id = []  # cve编号
    type = []  # 漏洞类型
    public_time = []  # 发布时间
    threat_type = []  # 威胁类型
    update_time = []  # 更新时间
    name_info = []  # 每个漏洞的名称
    describ = []  # 漏洞简介
    public = []  # 漏洞公告
    ref = []  # 参考
    cvss = []  # cvss分值
    usability = []  # 可利用性
    difrenced = []  # 受影响实体
    bd = []  # 补丁
    # 对于每一个链接，去爬取链接的页面
    for i in link:
        cnnvd = i.rsplit('=', 1)[1]
        html = getHTMLTEXT('http://www.cnnvd.org.cn' + i)
        soup = BeautifulSoup(html, 'html.parser')
        cve_name = u''
        title = soup.find_all('h2', style="")
        if title:
            cve_name = title[0].string
        # print "cve_name:   %s" % cve_name
        #  cve_id, cvss, usability
        cve_a = soup.find_all('a', target="_blank", rel="nofollow")
        cve = ''
        if cve_a:
            cve = cve_a[0].string.strip()
        cve_id.append(cve)

        cvss_value, usability_value = get_cvss(cve)
        cvss.append(cvss_value.strip())
        usability.append(usability_value.strip())

        # 漏洞简介， 漏洞公告，受攻击实体， 参考, 补丁
        ld_detail = soup.find_all('div', attrs={'class': "d_ldjj"})
        _desc = ''
        _pub = ''
        _ref = ''
        _diff = ''
        _bd = ''
        # print len(ld_detail)
        for co, des in enumerate(ld_detail):
            # print get_ldjj(des)
            tmp_value = get_ldjj(des)
            if co == 0:
                _desc = tmp_value
            elif co == 1:
                _pub = tmp_value
            elif co == 2:
                _ref = tmp_value
            elif co == 3:
                _diff = tmp_value
            elif co == 4:
                _bd = tmp_value

        # print _desc
        describ.append(_desc)
        public.append(_pub)
        difrenced.append(_diff)
        ref.append(_ref)
        bd.append(_bd)

        # print text
        text = soup.find_all('a', style="color:#4095cc;cursor:pointer;")
        S = []
        if len(text):
            # print len(text)
            for sn, t in enumerate(text):
                value = u'{}'.format(str(t.string).strip())

                if value:
                    S.append(value)
                else:
                    S.append(u'')
            cnnvd_id.append(cnnvd)
            # print S[0]
            level.append(S[0])
            # cve_id.append(S[1])
            type.append(S[1])
            public_time.append(S[2])
            threat_type.append(S[3])
            update_time.append(S[4])
            name_info.append(cve_name)

    for i in range(len(name_info)):
        sheet1.write(index + 1, 0, name_info[i].strip())
        sheet1.write(index + 1, 1, cnnvd_id[i].strip())
        sheet1.write(index + 1, 2, level[i].strip())
        sheet1.write(index + 1, 3, type[i].strip())
        sheet1.write(index + 1, 4, public_time[i].strip())
        sheet1.write(index + 1, 5, threat_type[i].strip())
        sheet1.write(index + 1, 6, update_time[i].strip())
        sheet1.write(index + 1, 7, cve_id[i].strip())
        sheet1.write(index + 1, 8, describ[i].strip())
        sheet1.write(index + 1, 9, public[i].strip())
        sheet1.write(index + 1, 10, ref[i])
        sheet1.write(index + 1, 11, difrenced[i].strip())
        sheet1.write(index + 1, 12, bd[i].strip())
        sheet1.write(index + 1, 13, cvss[i].strip())
        sheet1.write(index + 1, 14, usability[i].strip())
        index += 1
        print 'save cve ........%s' % index
    f.save("CVE_" + qstartdate + "_" + qenddate + ".xls")  # 保存文件


def all_page(url, n, f, sheet1, qstartdate, qenddate):
    link = []  # 每个漏洞的链接
    # 循环遍历每个网页
    count = 0
    for p in range(1, int(n) + 1):
        print "#################### %s page" % p
        if p % 100 == 0:
            print "wait 60s......................................................"
            time.sleep(60)
        html = getHTMLTEXT(url + str(p))
        soup = BeautifulSoup(html, 'html.parser')
        # 统计每个实体中具体漏洞的链接
        text = soup.find_all('a', attrs={'class': 'a_title2'})
        for i in text:
            try:
                href = i.attrs['href']
                if re.findall(r'.?CNNVD.?', href):
                    link.append(href)
                    # print count
                    count += 1
            except:
                continue
            if count % 10 == 0:
                print '============================================================'
                save_xls(count - 10, link, f, sheet1, qstartdate, qenddate)
                del link[:]
    save_xls(count - 10, link, f, sheet1, qstartdate, qenddate)


if __name__ == "__main__":
    during_date = [('2020-03-01', '2020-03-31')]

    # 全量更新
    # url = 'http://www.cnnvd.org.cn/web/vulnerability/queryLds.tag?'  # 全量搜索

    # 增量更新
    for item in during_date:
        qstartdate = item[0]
        qenddate = item[1]
        url = 'http://www.cnnvd.org.cn/web/vulnerability/queryLds.tag?qstartdate=' \
              + qstartdate + '&qenddate=' + qenddate  # 时间段搜索
        parsepage(0, url)
        turl = url + '&pageno='
        f, sheet1 = init_xls()
        print "start to get cve lib...... pagecount is  %s" % page[0][0]
        time.sleep(5)
        all_page(turl, page[0][0], f, sheet1, qstartdate, qenddate)
        del page[:]