# from weibo import APIClient
import json
from math import ceil
from __future__ import division
APP_KEY = 'Your APP_KEY'
CALLBACK_URL = '自定义'
APP_SECRET = 'Your APP_SECRET'
client = APIClient(app_key=APP_KEY, app_secret=APP_SECRET, redirect_uri=CALLBACK_URL)
# print client
# url = client.get_authorize_url()
# code的获取需要访问URL: https://api.weibo.com/oauth2/authorize?client_id='Your APP_KEY'&
#   redirect_uri=https://api.weibo.com/oauth2/default.html&response_type=code
# 其中client_id为APP_SECRET
code = 'xxxxxxxxxxxxxxxxxxxxxxxxx'
# 调用request_access_token方法获取token值，该方法接受一个我们前面获取的code参数
# 注意，在一个回话中r = client.request_access_token(code)只能调用一次，否则，token会发生变化
# 在获取到token值之后的操作中需对其注释掉
# r = client.request_access_token(code)
access_token = r.get('access_token')
expires_in = r.get('expires_in')
client.set_access_token(access_token, expires_in)
# 完成上面操作，便可以调用微博API了

# 以获取friendships数据为例
# 每一页显示的记录数count
count = 100

responsejson = client.friendships.friends.get(screen_name='iblusky', count=count)
# total_number关注用户总数
total_number  = responsejson.total_number
print '微博关注用户总数：', total_number
# next_cursor 下一页游标指向位置
next_cursor = responsejson.next_cursor
# 获取所有用户需要循环的次数icount
icount = int(ceil(total_number/count))
# print icount
i = 0
friendlists = []
while icount:
    
    friends = client.friendships.friends.get(screen_name='iblusky', count=count, cursor=i*count).users
    # 以json形式储存关注对象的信息

    for friend in friends:
        # 列表
        for k ,v in friend.items():
            if v == '' or v is None:
                del friend[k]
                continue
            try:
                friend[k] = v.encode('utf8')
            except:
                pass
        friendlists.append(friend)
    icount = icount-1
    i = i+1
# print friendlists
fp = open('weibojson.json', 'wt')
json.dump(friendlists, fp, indent=4,  ensure_ascii=False)
print '获取的用户数：', len(friendlists)
print json.dumps(friendlists, indent=4, encoding='utf8', ensure_ascii=False)
