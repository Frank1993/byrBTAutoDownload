# -*- coding: utf-8 -*-
 
import urllib
import urllib2
import cookielib
import re
#登录地址
byrBTLoginUrl = "http://bt.byr.cn/login.php"
byrBTLognPostUrl = "http://bt.byr.cn/takelogin.php"#  用于向bt网站提交登陆参数
checkCodeUrl = ''
loginresponse = ''
#post请求头部
headers = {
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language':'zh-CN,zh;q=0.8,en;q=0.6',
    'Cache-Control':'no-cache',
    'Connection':'keep-alive',
    'Content-Length':'100',
    'Content-Type':'application/x-www-form-urlencoded',
    'Cookie':'c_secure_ssl=bm9wZQ%3D%3D; Hm_lvt_9ea605df687f067779bde17347db8645=1441023042,1441243856,1441802547,1442025814; Hm_lpvt_9ea605df687f067779bde17347db8645=1442026717',
    'Host':'bt.byr.cn',
    'Origin':'http://bt.byr.cn',
    'Pragma':'no-cache',
    'Referer':'http://bt.byr.cn/login.php',
    'Upgrade-Insecure-Requests':'1',
    'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36'
}
#用户名，密码
username = "Frank1993"
password = "hpc4904288"
#请求数据包
postData = {   
    'username':username,
    'password':password,
    'imagehash':'ac570b8e4214094c6075ab30ccdb8b6c',
    'imagestring':'B6M15E'
}
#登录主函数
def loginToBYRBT():
    #cookie 自动处理器
    global checkCodeUrl
    cookiejar = cookielib.LWPCookieJar()#LWPCookieJar提供可读写操作的cookie文件,存储cookie对象
    cookieSupport= urllib2.HTTPCookieProcessor(cookiejar)
    opener = urllib2.build_opener(cookieSupport, urllib2.HTTPHandler)
    urllib2.install_opener(opener)
    #打开登陆页面
    byrBT = urllib2.urlopen(byrBTLoginUrl)
    resp = byrBT.read().decode("utf-8")
    #提取验证码地址
    pattern = r'img src="image\.php\?action=regimage&amp;imagehash=(\S*)"'
    imagehashList = re.findall(pattern, resp)
    imagehash = imagehashList[0]
    print "imagehash:", imagehash
    if imagehash:
        postData['imagehash']=imagehash
        print postData
        checkCodeUrl = 'http://bt.byr.cn/image.php?action=regimage&imagehash='+imagehash
        print checkCodeUrl
    if checkCodeUrl !='':
        getCheckCode(checkCodeUrl)
        #此时直接发送post数据包登录
        #sendPostData(tbLoginUrl, postData, headers)
        print postData
        sendPostData(byrBTLognPostUrl,postData,headers)
     

def getTorrentPage():
    torrentPage = urllib2.urlopen("http://bt.byr.cn/torrents.php").read().decode("utf-8")
    loginSuccessPattern=r'href="userdetails\.php\?id=\d*" class=\'User_Name\'><b>(\w*)'
    loginUser = re.findall(loginSuccessPattern,torrentPage)
    if loginUser[0]!=username:
        print 'login failed,now call the function loginToBYRBT()'
        loginToBYRBT()
    pattern = r'href="details\.php\?id=(\d*)&amp;hit=1&amp;dllist=1#leechers">(\d*)'
    torrentTuples = re.findall(pattern,torrentPage)
    sortedTorrentTuples=sorted(torrentTuples,key = lambda x: int(x[1]),reverse=True)[:10]
    for torrentTuple in sortedTorrentTuples:
        torrenturl = 'http://bt.byr.cn/download.php?id='+torrentTuple[0]
        torrent = urllib2.urlopen(torrenturl)
        torrentfile = torrent.read()
        path= "/Users/hu/development/%s.torrent" % torrentTuple[0]
        localTorrent = open(path,'wb')
        localTorrent.write(torrentfile)
        localTorrent.close()
        print '+'*20,
        print 'downloaded torrent:id %s hotDegree  %s' % torrentTuple,
        print '+'*20







def sendPostData(url, data, header):
    print "+"*20+"sendPostData"+"+"*20
    data = urllib.urlencode(data)      
    request = urllib2.Request(url, data, header)
    loginresponse = urllib2.urlopen(request)
    getTorrentPage()




def getCheckCode(url):
    print "+"*20+"getCheckCode"+"+"*20
    response = urllib2.urlopen(url)
    status = response.getcode()
    picData = response.read()
     
    path = "/Users/hu/development/image.jpeg"
    if status == 200:
        localPic = open(path, "wb")
        localPic.write(picData)
        localPic.close() 
        print "请到%s,打开验证码图片"%path  
        checkCode = raw_input("请输入验证码：")
        print checkCode, type(checkCode)
        postData["imagestring"] = checkCode
    else:
        print "failed to get Check Code, status: ",status
 
if __name__ == "__main__":   
    getTorrentPage()
