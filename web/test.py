# -*- coding:utf-8 -*-
#author:菜鸟小白的学习分享
import requests, base64
def get_access_token():
    url = 'https://aip.baidubce.com/oauth/2.0/token'
    data = {
        'grant_type': 'client_credentials',  # 固定值
        'client_id': 'dW4CnnfGbvg9jKpqhl1MNaQ8',  # 在开放平台注册后所建应用的API Key
        'client_secret': 'BuX8qH0Filun7pqsbehpeiqzFOuBsHf5'  # 所建应用的Secret Key
    }
    res = requests.post(url, data=data)
    res = res.json()
    print(res)
    access_token = res['access_token']
    return access_token


def get_config():
    img_before = input("请输入当前文件夹下需要处理的图片名称：")
    process_action = ['','selfie_anime','colourize','style_trans']
    print("支持以下处理动作：\n1:为人像动漫化\n2:图像上色\n3:为图像风格化")
    # 处理动作： selfie_anime 为人像动漫化，colourize 图像上色，style_trans 为图像风格化
    i = int(input("请输入需要处理的动作："))
    """
    cartoon：卡通画风格
    pencil：铅笔风格
    color_pencil：彩色铅笔画风格
    warm：彩色糖块油画风格
    wave：神奈川冲浪里油画风格
    lavender：薰衣草油画风格
    mononoke：奇异油画风格
    scream：呐喊油画风格
    gothic：哥特油画风格"""
    others = ['','cartoon','pencil','color_pencil','warm','wave','lavender','mononoke','scream','gothic']
    j = 0
    if process_action[i] == 'style_trans':
        print("支持转化的风格有：\n\
            1：卡通画风格\n\
            2：铅笔风格\n\
            3：彩色铅笔画风格\n\
            4：彩色糖块油画风格\n\
            5：神奈川冲浪里油画风格\n\
            6：薰衣草油画风格\n\
            7：奇异油画风格\n\
            8：呐喊油画风格\n\
            9：哥特油画风格\n")
        j = int(input("请输入需要转化的风格类型（数字）："))
    return img_before,process_action[i],others[j]


def image_process(img_before, img_after, how_to_deal,others):
    # 函数的三个参数，一个是转化前的文件名，一个是转化后的文件名，均在同一目录下，第三个是图像处理能力选择
    request_url = 'https://aip.baidubce.com/rest/2.0/image-process/v1/' + how_to_deal
    file = open(img_before, 'rb')  # 二进制读取图片
    origin_img = base64.b64encode(file.read())  # 将图片进行base64编码
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    data = {
        'access_token': get_access_token(),
        'image': origin_img,
        'option': others
    }
    res = requests.post(request_url, data=data, headers=headers)
    res = res.json()

    if res:
        f = open(img_after, 'wb')
        after_img = res['image']
        after_img = base64.b64decode(after_img)
        f.write(after_img)
        f.close()


if __name__ == '__main__':
    # 选择输入信息
    img_before, process_action, others = get_config()
    img_after = img_before.split('.')  # 将原文件名分成列表
    img_after = img_after[0] + '_1.' + img_after[1]  # 新生成的文件名为原文件名上加 _1
    image_process(img_before, img_after, process_action,others)
    print('done!')
