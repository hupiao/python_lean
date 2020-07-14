# -*- coding: utf-8 -*-
import logging
from bs4 import BeautifulSoup

test = "<!DOCTYPE html><html><title>我的第一个 HTML 页面</title><body><p>body 元素的内容会显示在浏览器中。</p></body></html>"
tt =  "财务部声明：\r\n\r\n需开票报销，票额与实际消费金额一致，费用包括：食品、办公用品，单位名称需正确，其他采购部门如有需要，进一步咨询！\r\n\r\n互惠互利，合作共赢，禁止转账\r\n\r\n标题文档\r\n\r\n \r\n\r\n \r\n\r\n移动电话：——\r\n\r\n"
# tt = 'fadfadfa'
content = ''
try:
    soup = BeautifulSoup(content, "html.parser", from_encoding='utf-8')
    prefix = '<p style="text-align: justify; font-size: 10.5pt;font-family: 等线;">' \
             '<span style="text-decoration: underline rgb(5,99,193);background: red;' \
             'color: white;border-radius: 3px;padding: 3px;">'
    postfix = '</span></p>'
    plain_attribute = ['222.186.190.23:8080/Consys21.dll']
    if plain_attribute:
        for pa in plain_attribute:
            content = content.replace(pa, prefix + pa + postfix)
except Exception as e:
    logging.error(e)
    print e
