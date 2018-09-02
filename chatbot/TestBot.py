import requests
import itchat
from itchat.content import *
import datetime

KEY = '2c242b43e94a4e0ca984629828d4e164'
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
    finalMsg = ''
    defaultReply = 'I received: ' + finalMsg
    reply = ''
    msgNickName = msg.User.RemarkName or msg.User.NickName
    time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') +" : "
    try:
        for m in msg['Text']:
            finalMsg += m
        recordfile = open("D://wechatrecord/"+msgNickName+'.txt',mode = 'a+',encoding='utf-8')
        recordfile.write('\n'+time+finalMsg)
    except BaseException as e:
        print(e)
    finally:
        # 如果图灵Key出现问题，那么reply将会是None
        #reply = get_response(msg['Text'])
        # a or b的意思是，如果a有内容，那么返回a，否则返回b
        # 有内容一般就是指非空或者非None，你可以用`if a: print('True')`来测试
        print('RECEIVED:' + finalMsg)
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
itchat.run()
