import requests
import time

def photo_download():
    ph_http = input("小主，请输入图像链接：")
    ph_name = input("请为图片命名：")
    print('正在下载高清图片，请稍后！')
    time.sleep(1)

    re1 = requests.get(url=ph_http)  # URL要按一般格式写，不能自行加入空格

    with open(f'{ph_name}.jpg', 'wb') as new_file:  # 站点图标格式  .ico  以二进制格式操作
        file5 = new_file.write(re1.content)  # 直接写入=保存

    print("下载完成")
    time.sleep(1)

photo_download()


#可以将随机命名加到函数中，节省自己命名的时间
