import requests
from cookies import cookie
import re
import time

start_url = 'http://music.163.com/discover/toplist'

headers = {
	'Accept': '*/*',
    'Accept-Encoding': 'gzip,deflate,sdch',
    'Accept-Language': 'zh-CN,zh;q=0.8',
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Host': 'music.163.com',
    'Referer': 'http://music.163.com/search/',
    'User-Agent':
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'
}

html = requests.get(start_url, headers=headers, cookies=cookie)
html = html.text

print html

musicId_box = set()
commentId_box = set()

def parse_playList(html):
    # get each play list id
    playlist = re.findall("toplist\?id\=(\d+)", html)
    for each in playlist:
        parse_musicId(each, html)
        time.sleep(2)
        

def parse_musicId(each, html):

    url = 'http://music.163.com/discover/toplist?id={}'.format(each)

    # get each music id
    musicId = re.findall("song\?id\=(\d+)", html)
    for each in musicId:
        print 'musicId:' + each
        musicId_box.add(each.encode('utf-8'))

    # get comment api id
    commentId = re.findall("R\_SO\_4\_(\d+)", html)
    for each in commentId:
        print 'commentId' + each
        commentId_box.add(each.encode('utf-8'))
    
    save_to_file(musicId_box, 'musicId_box')
    save_to_file(commentId, 'commentId')
        
        
        
def save_to_file(data, name):
    parse_data = name + ' = ' + str(data)
    with open('%s.py' % name, 'w') as f:
        f.write(parse_data)


parse_playList(html)