#!/usr/bin/env python
#encoding:utf-8
import urllib.request
import urllib.error
import re
import os
import sys
from bs4 import BeautifulSoup
import json
import time
import http.cookiejar


FontType = sys.getfilesystemencoding()
RootUrl = "http://localhost:3000"
LoginUrl = "/login/cellphone?phone=x&password=x"
FetchSongListUrl = "/playlist/detail?id="
FooSongListId = "2434340328"
BarSongListId = "2435224926"
OurSongListId = "2435116800"
AddSongUrl = "/playlist/tracks?op=add&pid={}&tracks={}"

def getHtmlData(url):
    url = (url+"&timestamp=")+str(int(time.time()))
    print(url)
    # 欺骗为 iPhone/iPad 的请求
    req = urllib.request.Request(
    	url,
    	data = None,
    	headers = {
            'User-Agent':'AppleWebKit/537.36'
        }
    )
    try:
        response = urllib.request.urlopen(req)
    except urllib.error.HTTPError as e:
        print(e)
        return

    data = response.read()

    data = data.decode('utf-8')

    # print(data)

    return data

def getBeautilfulHtmlData(url):
    data = getHtmlData(url)

    bs = BeautifulSoup(data, 'html.parser')
    print(bs.encode("UTF-8"))

    return bs

def getJsonHtmlData(url):
	data = getHtmlData(url)
	jsonData = json.loads(data)
	return jsonData

def fetchSongList(url):
	songList = getJsonHtmlData(url)
	songIdList = []
	if songList["code"] == 200:
		for songInfo in songList["playlist"]["trackIds"]:
			songIdList.append(songInfo["id"])
	print(songIdList)
	return songIdList

def getDiffSongs():
	FooSongList = fetchSongList(RootUrl+FetchSongListUrl+FooSongListId)
	BarSongList = fetchSongList(RootUrl+FetchSongListUrl+BarSongListId)
	OurSongList = fetchSongList(RootUrl+FetchSongListUrl+OurSongListId)

	ourNewSongList = list(set(FooSongList+BarSongList))
	print("ourNewSongList:")
	print(ourNewSongList)
	diffSongList = list(set(ourNewSongList)-set(OurSongList));
	print("diffSongList:")
	print(diffSongList)
	return diffSongList


def addSongsToOurSongList(diffSongs):
	MyCookie = http.cookiejar.CookieJar()  # 声明一个CookieJar对象实例来保存cookie
	handler = urllib.request.HTTPCookieProcessor(MyCookie)  # 利用urllib2库的HTTPCookieProcessor对象来创建cookie处理器
	opener = urllib.request.build_opener(handler)  # 通过handler来构建opener
	head = {'User-Agnet': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36', 
	'Connection': 'keep-alive',
	'Cookie':'undefined; __remember_me=true; appver=1.5.9; os=osx; channel=netease; osver=%E7%89%88%E6%9C%AC%2010.13.2%EF%BC%88%E7%89%88%E5%8F%B7%2017C88%EF%BC%89; __csrf=331f6765780ea77485d94d0e08305f18; MUSIC_U=b7d4e6b04f9e2997dc1584fcaf7f6acfab1cd2916269b12d37f426111a660bad845d0aa8b8d664683f72ca17793d607efe2897047e8106fb'}

	#创建Request对象
	loginRequest = urllib.request.Request(RootUrl+LoginUrl, data=None, headers=head)

	# loginResult = json.loads(response.read())
	

	# print(loginResult)
	
	# if loginResult["code"] == 200:
	# 	print("Login Success")
	# else:
	# 	print("Login Fail"+json.dumps(loginResult))


	diffSongsString = ','.join(str(e) for e in diffSongs)
	addUrl = (RootUrl+AddSongUrl).format(OurSongListId, diffSongsString)

	addRequest = urllib.request.Request(addUrl, data=None, headers=head)
	
	loginResponse = opener.open(loginRequest);

	loginResult = json.loads(loginResponse.read().decode('utf-8'))

	print(json.dumps(loginResult));	

	addResponse = urllib.request.urlopen(addRequest);

	addResult = json.loads(addResponse.read().decode('utf-8'))

	print(json.dumps(addResult));

	for item in MyCookie:
		print('Name = ' + item.name)
		print('Value = ' + item.value)

	print(addResult);
	if addResult["code"] == 200:
		print("Add Success")
	else:
		print("Add Fail. errorCode:{} errorMsg:{}".format(addResult["code"], addResult["msg"]))

def main():
	diffSongList = getDiffSongs()
	addSongsToOurSongList(diffSongList)

if __name__=="__main__":
    main()
