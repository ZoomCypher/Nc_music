
#coding = utf-8
from Crypto.Cipher import AES
from pymongo import MongoClient
import base64
import requests
import json
import time

class Get_comment(object):
    
    def __init__(self):
        
        self.headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.91 Safari/537.36',
                'Cookie': 'appver=1.5.0.75771;',
                'Referer': 'http://music.163.com/'
                }
        self.id = 35382003
        self.offset = 0
        self.url = "http://music.163.com/weapi/v1/resource/comments/R_SO_4_%s?csrf_token=" % self.id

        self.second_param = "010001"
        self.third_param = "00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7"
        self.forth_param = "0CoJUm6Qyw8W8jud"

        self.conection = MongoClient('localhost', 27017)
        self.db = self.conection['nw_music']
        self.item = self.db['items']

        self.switch = True

    def get_params(self):
        first_param = "{rid:\"\", offset:\"%s\", total:\"true\", limit:\"20\", csrf_token:\"\"}" % self.offset
        iv = "0102030405060708"
        first_key = self.forth_param
        second_key = 16 * 'F'
        h_encText = self.AES_encrypt(first_param, first_key, iv)
        h_encText = self.AES_encrypt(h_encText, second_key, iv)
        return h_encText

    def get_encSecKey(self):
        encSecKey = "257348aecb5e556c066de214e531faadd1c55d814f9be95fd06d6bff9f4c7a41f831f6394d5a3fd2e3881736d94a02ca919d952872e7d0a50ebfa1769a7a62d512f5f1ca21aec60bc3819a9c3ffca5eca9a0dba6d6f7249b06f5965ecfff3695b54e1c28f3f624750ed39e7de08fc8493242e26dbc4484a01c76f739e135637c"
        return encSecKey
    
    def AES_encrypt(self, text, key, iv):
        pad = 16 - len(text) % 16
        text = text + pad * chr(pad)
        encryptor = AES.new(key, AES.MODE_CBC, iv)
        encrypt_text = encryptor.encrypt(text)
        encrypt_text = base64.b64encode(encrypt_text)
        return encrypt_text

    def get_json(self, params, encSecKey):
        data = {
            "params": params,
            "encSecKey": encSecKey
        }
        response = requests.post(self.url, headers=self.headers, data=data)
        return response.content

    def scheduler(self):
        print 'start request.....'
        params = self.get_params()
        encSecKey = self.get_encSecKey()
        json_text = self.get_json(params, encSecKey)
        json_dict = json.loads(json_text)
        # out loop
        if len(json_dict['comments']) == 0:
            self.switch = False
            self.run()
        self.parse_comment(json_dict)

    def parse_comment(self, json_dict):
        print 'start parsing......'
        for comment in json_dict['comments']:
            try:
                # item = {}
                comment = comment['content'].encode('utf-8', 'ignore')
                print comment
                # item['comment'] = comment 
                # user = comment['user']['nickname'].encode('utf-8', 'ignore')
                # item['nickname'] = user 
                # likedCount = comment['likedCount'].encode('utf-8', 'ignore')
                # item['likedCount'] = likedCount 
            except Exception:
                pass
            # print item
            # self.save_comment(item)
    
    def save_comment(self, data):
        pass
        # try:
        #     self.item.insert(dict(item))
        # except Exception:
        #     pass
    
    def run(self):
        while self.switch:
            print 'calling scheduler.....'
            self.scheduler()
            time.sleep(2)            
            self.offset += 20
        print 'over!'
            
        
        
        
        
        


if __name__ == "__main__":
    
    comm = Get_comment()
    comm.run()
    
    