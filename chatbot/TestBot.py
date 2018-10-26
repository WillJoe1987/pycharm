import requests
import itchat
from itchat.content import *
import datetime
import os
from ui.mouth import HelloFrame
import wx
#KEY = '6be4aa0dff5741d48c1000961c6c6b1a'#李特尔飞什
#KEY = '2c242b43e94a4e0ca984629828d4e164'#东妹
robots = {
    '李特尔飞什': {
        'KEY' : '6be4aa0dff5741d48c1000961c6c6b1a'
    },
    '东妹': {
        'KEY' : '2c242b43e94a4e0ca984629828d4e164'
    },
    '阿咪':{
        'KEY' : '13d19972340946e5b268dcf77d089f11'
    }
}

friends_robots = {}

friends = None
#current_name=''
base_path = 'D:/wechatrecord/'
robot_friends = ['宝儿','李特尔飞什','Cherry','全万鹏','尚吉峰','郑春','李白','刘爽']
tolist = ['孔郢','刘金文','李晶伟']
tjyhkjb = ['代明君','姚毅','赵尔航','赵子龙','魏莎','王峰','陈云冲-天津银行']


app = wx.App()
frm = HelloFrame(None, title='Hello World 2')

def get_robots_key_by_friends(msg):
    if check_has_robot(msg):
        return friends_robots[msg.FromUserName]
    else:
        return init_friend_robot(msg, '李特尔飞什')

def init_friend_robot(msg, robot = '李特尔飞什'):
    friends_robots[msg.FromUserName] = robots[robot]['KEY']
    itchat.send_msg('我是机器人：'+robot,msg.FromUserName)
    return friends_robots[msg.FromUserName]

def check_and_init_robot(msg):
    content = get_msg_content(msg)
    robots_name = '李特尔飞什'
    if content[0:4] == '机器人：' or content[0:4] == '机器人:':
        for key in robots :
            if content.find(key) > 1:
                robots_name = key
                break
        return init_friend_robot(msg, robots_name)

def check_and_close_robot(msg):
    content = get_msg_content(msg)
    if content == '闭嘴机器人':
        try :
            del friends_robots[msg.FromUserName]
        finally:
            return

def check_has_robot(msg):
    try:
        friends_robots[msg.FromUserName]
    except BaseException as e:
        return False
    return True

def get_friend_name(friend_key_name, friends = friends):
    if friends is None:
        friends = itchat.get_friends()
    for f in friends:
        if f.UserName == friend_key_name:
            return f.RemarkName or f.NickName
    return friend_key_name

def get_actual_name(msg):
    if hasattr(msg, 'ActualNickName'):
        return msg.ActualNickName
    else :
        return False

def get_current_name():
    return friends[0].NickName

def redirect_msg(finalMsg, tolists=tolist):
    theToList = tolists
    if theToList is None or theToList.__len__() == 0:
        theToList = tolist
    for user in theToList:
        fr = itchat.search_friends(user)
        for f in fr :
            itchat.send_msg(finalMsg, f.userName)

def send_file(file_dir, tolists=tolist):
    theToList = tolists
    if theToList is None or theToList.__len__() == 0:
        theToList = tolist
    for user in theToList:
        fr = itchat.search_friends(user)
        for f in fr:
            itchat.send_file(file_dir, f.userName)

def write_msg(msg):
    finalMsg = ''
    try:
        time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + " : "
        user_path = base_path+current_name
        if(not os.path.exists(user_path)):
            os.mkdir(user_path)
        message_file_name = user_path+'/'+(msg.User.RemarkName or msg.User.NickName)+'.txt'
        message_file = open(message_file_name,mode='a+',encoding='utf-8')
        aNickName = get_actual_name(msg) or get_friend_name(msg.FromUserName)
        finalMsg = get_msg_content(msg)
        finalMsg = time+'['+aNickName+'] '+finalMsg
        message_file.write('\n'+finalMsg)
    except BaseException as e:
        print(e)
    finally:
        return finalMsg

def get_msg_content(msg):
    finalMsg = ''
    for m in msg['Text']:
        finalMsg += m
    return finalMsg

def get_response(msg,KEY):
    # 构造了要发送给服务器的数据
    # 使用图灵机器人提供的接口
    apiUrl = 'http://www.tuling123.com/openapi/api'#v1
    #apiUrl = 'http://openapi.tuling123.com/openapi/api/v2'
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
        return r.get('text'), r.get('url', '')
    # 为了防止服务器没有正常响应导致程序异常退出，这里用try-except捕获了异常
    # 如果服务器没能正常交互（返回非json或无法连接），那么就会进入下面的return
    except BaseException as e:
        print(e)
        # 将会返回一个None
        return

# 使用装饰器
@itchat.msg_register(TEXT ,isFriendChat=True, isGroupChat=True, isMpChat=False)
def tuling_reply(msg, KEY = '6be4aa0dff5741d48c1000961c6c6b1a'):
    # 为了保证在图灵Key出现问题的时候仍旧可以回复，这里设置一个默认回复
    # 如果图灵Key出现问题，那么reply将会是None

    # a or b的意思是，如果a有内容，那么返回a，否则返回b
    # 有内容一般就是指非空或者非None，你可以用`if a: print('True')`来测试
    finalMsg = write_msg(msg)
    real_from_user = msg.User.RemarkName or msg.User.NickName
    if real_from_user in tjyhkjb :
        redirect_msg(finalMsg)
    print('【'+real_from_user+'】'+finalMsg)
    frm.push_msg('【'+real_from_user+'】'+finalMsg)
    #print('REPLY:' + reply or defaultReply)
    # itchat.send(reply or defaultReply, msg['FromUserName'])
    aNickName = get_actual_name(msg) or get_friend_name(msg.FromUserName)
    if aNickName in robot_friends :
        check_and_close_robot(msg)
        check_and_init_robot(msg)
        if check_has_robot(msg):
            reply, url = get_response(msg['Text'],get_robots_key_by_friends(msg))
            print('【机器人】to【'+real_from_user+'】' + reply + url)
            return reply+url
        else:
            return False
    else:
        return False #reply or defaultReply

@itchat.msg_register([PICTURE, RECORDING, ATTACHMENT, VIDEO],isFriendChat=True, isGroupChat=True, isMpChat=False)
def get_files(msg):
    # me = itchat.get_friends()[0]
    # directory = get_msg_directory(me, msg)
    user_path = base_path + current_name + '/' + (msg.User['RemarkName'] or msg.User['NickName'])
    if (not os.path.exists(user_path)):
        os.mkdir(user_path)
    aUserName = get_actual_name(msg) or get_friend_name(msg.FromUserName)
    aNickName = (msg.User.RemarkName or msg.User.NickName)
    aFileName = msg.FileName
    time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + " : "
    print('【'+aNickName+'】'+time+' : '+'['+aUserName+']::send file:' + '【'+aFileName+'】')
    os.chdir(user_path)
    msg.download(msg.FileName)
    # msg['Text'](msg['FileName'])
    real_from_user = msg.User.RemarkName or msg.User.NickName
    if real_from_user in tjyhkjb:
        red_msg = "["+aUserName+"]：发来文件:["+msg.FileName+"]"
        redirect_msg(red_msg)
        send_file(user_path+"/"+msg.FileName)
        # print(msg['Text'](msg['FileName']))
        print(user_path+"/"+msg.FileName)
    return False
# 为了让实验过程更加方便（修改程序不用多次扫码），我们使用热启动
itchat.auto_login(hotReload=True)
friends = itchat.get_friends()
current_name = friends[0].NickName
os.chdir(base_path+'/'+current_name)
#frm.Show()
#app.MainLoop()
itchat.run()
