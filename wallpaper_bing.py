import requests, json, time, os, win32api, win32gui, win32con, sys, datetime, random
from contextlib import closing
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from pymouse import PyMouse
print('Author:Mister魏 Version:1.0 CreateTime:2018.08.09')
m=PyMouse()
x_dim,y_dim=m.screen_size()
resolution=str(x_dim)+'x'+str(y_dim)
target='http://cn.bing.com/HPImageArchive.aspx?format=js&idx=0&n=7'
req=requests.get(url=target,verify=False)
#print(type(req.text))
json_pic=json.loads(req.text)
#print(type(json_pic))
url=json_pic["images"]
copyright_a=json_pic["images"]
path=os.getcwd()+'/wallpaper_bing_temp'
try:
    os.mkdir(path)
except FileExistsError:
    pass
win32api.SetFileAttributes(path,win32con.FILE_ATTRIBUTE_HIDDEN)#隐藏图片文件夹
for each in url:
    copyright_a=each["enddate"]+each["copyright"]
    if '(' in copyright_a:
        copyright_b=copyright_a.rsplit('(',1)[0].rstrip()
    elif '（' in copyright_a:
        copyright_b=copyright_a.rsplit('（',1)[0].rstrip()
    else:
        copyright_b=copyright_a
    url_b='http://cn.bing.com'+each["url"]
    #url_b=url_a.replace('1920x1080',resolution,1)#replace替换字符串的时候，需要重新赋值给变量，因为在python中字符串是不可变对象
    filename=each["url"].rsplit('/',1)[1]
    #print(copyright_b,'=====>',url_b)
    time.sleep(random.randint(1,2))
    if filename.rsplit('.',1)[0].rsplit('_',1)[1]=='1920x1080':
        #根据获取的图片地址下载图片
        with closing(requests.get(url=url_b,stream=True,verify=False)) as r:     
            with open(path+'/'+copyright_b+'.jpg','ab+') as f:
                for chunk in r.iter_content(chunk_size=3072):
                    if chunk:
                        f.write(chunk)
                        win32api.SetFileAttributes(path+'/'+copyright_b+'.jpg',win32con.FILE_ATTRIBUTE_HIDDEN)#隐藏图片
                        f.flush()
                print('已下载bing图片:',copyright_b+'.jpg')
                sys.stdout.flush()
    else:
        pass
f=os.listdir(path)
f.sort(reverse=False)
time_today=datetime.datetime.now().strftime("%Y%m%d")
for i in f:
    jpg_path=path+'/'+i
    ctime=os.path.getctime(jpg_path)
    ctime_f=time.strftime("%Y%m%d",time.localtime(ctime))
    if i.rsplit('.',1)[1]=='jpg' and ctime_f==time_today:
        #把图片格式统一转换成bmp格式,写上文字信息,并放在源图片的同一目录
        bmp_image=Image.open(jpg_path)
        bmp_path=path+'/'+i.rsplit('.',1)[0]+'.bmp'
        font=ImageFont.truetype(path+'/msyhbd.ttf',18)
        draw=ImageDraw.Draw(bmp_image)
        draw.text((bmp_image.size[0]*0.618,bmp_image.size[1]*0.926),i.rsplit('.',1)[0][8:],(255,255,255),font=font)            
        draw=ImageDraw.Draw(bmp_image)
        bmp_image.save(bmp_path,"BMP")
        win32api.SetFileAttributes(bmp_path,win32con.FILE_ATTRIBUTE_HIDDEN)#隐藏图片
        os.remove(jpg_path)
    elif i.rsplit('.',1)[1]=='py' or i.rsplit('.',1)[1]=='ttf' or i.rsplit('.',1)[1]=='exe':
        pass
    else:
        os.remove(jpg_path)
        print(i,'createtime:',ctime_f,'已删除')
wp=os.listdir(path)
wp.sort(reverse=True)
while True:
    for b in wp:
        if b.rsplit('.',1)[1]=='bmp':
            bmp_path=path+'/'+b
            os.system('cls')
            print('当前桌面背景:',b)
            sys.stdout.flush()            
            #打开指定注册表路径
            regKey = win32api.RegOpenKeyEx(win32con.HKEY_CURRENT_USER,"Control Panel\\Desktop",0,win32con.KEY_SET_VALUE)
            #最后的参数:2拉伸,0居中,6适应,10填充,0平铺
            win32api.RegSetValueEx(regKey,"WallpaperStyle", 0, win32con.REG_SZ, "2")
            #最后的参数:1表示平铺,拉伸居中等都是0
            win32api.RegSetValueEx(regKey, "TileWallpaper", 0, win32con.REG_SZ, "0")
            # refresh screen刷新桌面
            win32gui.SystemParametersInfo(win32con.SPI_SETDESKWALLPAPER,bmp_path,win32con.SPIF_SENDWININICHANGE)
            time.sleep(random.randint(21,61))
        else:
            pass
#小白试手,欢迎大神改进
        
