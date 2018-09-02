import requests
import itchat
from itchat.content import *
import datetime
import os

KEY = '2c242b43e94a4e0ca984629828d4e164'

friends = None
current_name=''
base_path = 'D:/wechatrecord/'

def get_friend_name(friend_key_name, friends = friends):
    if friends is None:
        friends = itchat.get_friends()
    for f in friends:
        if f.UserName == friend_key_name:
            return f.RemarkName or f.NickName
    return friend_key_name

def get_current_name():
    return friends[0].NickName

def write_msg(msg):
    finalMsg = ''
    try:
        time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + " : "
        user_path = base_path+current_name
        if(not os.path.exists(user_path)):
            os.mkdir(user_path)
        message_file_name = user_path+'/'+(msg.User.RemarkName or msg.User.NickName)+'.txt'
        message_file = open(message_file_name,mode='a+',encoding='utf-8')
        for m in msg['Text']:
            finalMsg += m
        finalMsg = time+get_friend_name(msg.FromUserName)+' '+finalMsg
        message_file.write('\n'+finalMsg)
    except BaseException as e:
        print(e)
    finally:
        return finalMsg

def get_response(msg):
    # 构造了要发送给服务器的数据
    # 使用图灵机器人提供的接口
    apiUrl = 'http://www.tuling123.com/openapi/api'
    #一个发动的api的数据
    data = {
        'key'    : KEY,
        'info'   : msg,
        'userid' : 'wechat-robot',
    }
    try:
        #使用post方法去请求
        r = requests.post(apiUrl, data=data).json()
        # 字典的get方法在字典没有'text'值的时候会返回None而不会抛出异常
        return r.get('text')
    # 为了防止服务器没有正常响应导致程序异常退出，这里用try-except捕获了异常
    # 如果服务器没能正常交互（返回非json或无法连接），那么就会进入下面的return
    except:
        # 将会返回一个None
        return

# 使用装饰器
@itchat.msg_register(TEXT,isFriendChat=True, isGroupChat=True, isMpChat=True)
def tuling_reply(msg):
    # 为了保证在图灵Key出现问题的时候仍旧可以回复，这里设置一个默认回复
    # 如果图灵Key出现问题，那么reply将会是None
    #reply = get_response(msg['Text'])
    # a or b的意思是，如果a有内容，那么返回a，否则返回b
    # 有内容一般就是指非空或者非None，你可以用`if a: print('True')`来测试
    finalMsg = write_msg(msg)
    print(finalMsg)
    #print('REPLY:' + reply or defaultReply)
    # itchat.send(reply or defaultReply, msg['FromUserName'])
    return False #reply or defaultReply

@itchat.msg_register([PICTURE, RECORDING, ATTACHMENT, VIDEO])
def get_files(msg):
    # me = itchat.get_friends()[0]
    # directory = get_msg_directory(me, msg)
    msg.download(msg.FileName)
    # msg['Text'](msg['FileName'])
    return False

# 为了让实验过程更加方便（修改程序不用多次扫码），我们使用热启动
itchat.auto_login(hotReload=True)
friends = itchat.get_friends()
current_name = friends[0].NickName
itchat.run()
