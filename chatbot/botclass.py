import requests
import itchat
from itchat.content import *
import datetime
import os

class wljbot():
    # util config
    robots = {
        '李特尔飞什': {
            'KEY': '6be4aa0dff5741d48c1000961c6c6b1a'
        },
        '东妹': {
            'KEY': '2c242b43e94a4e0ca984629828d4e164'
        },
        '阿咪': {
            'KEY': '13d19972340946e5b268dcf77d089f11'
        }
    }
    autoLogon = True
    hotReload = True
    # mid var
    friends_robots = {}
    # session config
    friends = []
    current_name = 'None login'
    base_path = 'D:/wechatrecord/'
    robot_friends = ['宝儿', '李特尔飞什', 'Cherry', '全万鹏', '尚吉峰', '郑春', '李白', '刘爽']
    tolist = ['孔郢', '刘金文', '李晶伟']
    tjyhkjb = ['代明君', '姚毅', '赵尔航', '赵子龙', '魏莎', '王峰', '陈云冲-天津银行']

    def __init__(self):
        pass

    def get_files(self, msg):
        # me = itchat.get_friends()[0]
        # directory = get_msg_directory(me, msg)
        user_path = self.base_path + self.current_name + '/' + (msg.User['RemarkName'] or msg.User['NickName'])
        if (not os.path.exists(user_path)):
            os.mkdir(user_path)
        aUserName = self.get_actual_name(msg) or self.get_friend_name(msg.FromUserName)
        aNickName = (msg.User.RemarkName or msg.User.NickName)
        aFileName = msg.FileName
        time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + " : "
        print('【' + aNickName + '】' + time + ' : ' + '[' + aUserName + ']::send file:' + '【' + aFileName + '】')
        os.chdir(user_path)
        msg.download(msg.FileName)
        # msg['Text'](msg['FileName'])
        real_from_user = msg.User.RemarkName or msg.User.NickName
        if real_from_user in self.tjyhkjb:
            red_msg = "[" + aUserName + "]：发来文件:[" + msg.FileName + "]"
            self.redirect_msg(red_msg)
            self.send_file(user_path + "/" + msg.FileName)
            # print(msg['Text'](msg['FileName']))
            print(user_path + "/" + msg.FileName)
        return False

    def tuling_reply(self, msg, KEY='6be4aa0dff5741d48c1000961c6c6b1a'):
        # 为了保证在图灵Key出现问题的时候仍旧可以回复，这里设置一个默认回复
        # 如果图灵Key出现问题，那么reply将会是None

        # a or b的意思是，如果a有内容，那么返回a，否则返回b
        # 有内容一般就是指非空或者非None，你可以用`if a: print('True')`来测试
        finalMsg = self.write_msg(msg)
        real_from_user = msg.User.RemarkName or msg.User.NickName
        if real_from_user in self.tjyhkjb:
            self.redirect_msg(finalMsg)
        print('【' + real_from_user + '】' + finalMsg)
        # print('REPLY:' + reply or defaultReply)
        # itchat.send(reply or defaultReply, msg['FromUserName'])
        aNickName = self.get_actual_name(msg) or self.get_friend_name(msg.FromUserName)
        if aNickName in self.robot_friends:
            self.check_and_close_robot(msg)
            self.check_and_init_robot(msg)
            if self.check_has_robot(msg):
                reply, url = self.get_response(msg['Text'], self.get_robots_key_by_friends(msg))
                print('【机器人】to【' + real_from_user + '】' + reply + url)
                return reply + url
            else:
                return False
        else:
            return False  # reply or defaultReply

    def run(self):
        itchat.auto_login(hotReload=self.hotReload)
        self.friends = itchat.get_friends()
        self.current_name = self.friends[0].NickName
        os.chdir(self.base_path + '/' + self.current_name)
        itchat.run()

    def get_response(msg, KEY):
        # 构造了要发送给服务器的数据
        # 使用图灵机器人提供的接口
        apiUrl = 'http://www.tuling123.com/openapi/api'  # v1
        # apiUrl = 'http://openapi.tuling123.com/openapi/api/v2'
        # 一个发动的api的数据
        data = {
            'key': KEY,
            'info': msg,
            'userid': 'wechat-robot',
        }
        try:
            # 使用post方法去请求
            r = requests.post(apiUrl, data=data).json()
            # 字典的get方法在字典没有'text'值的时候会返回None而不会抛出异常
            return r.get('text'), r.get('url', '')
        # 为了防止服务器没有正常响应导致程序异常退出，这里用try-except捕获了异常
        # 如果服务器没能正常交互（返回非json或无法连接），那么就会进入下面的return
        except BaseException as e:
            print(e)
            # 将会返回一个None
            return

    def get_msg_content(self, msg):
        finalMsg = ''
        for m in msg['Text']:
            finalMsg += m
        return finalMsg

    def write_msg(self, msg):
        finalMsg = ''
        try:
            time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + " : "
            user_path = self.base_path + self.current_name
            if (not os.path.exists(user_path)):
                os.mkdir(user_path)
            message_file_name = user_path + '/' + (msg.User.RemarkName or msg.User.NickName) + '.txt'
            message_file = open(message_file_name, mode='a+', encoding='utf-8')
            aNickName = self.get_actual_name(msg) or self.get_friend_name(msg.FromUserName)
            finalMsg = self.get_msg_content(msg)
            finalMsg = time + '[' + aNickName + '] ' + finalMsg
            message_file.write('\n' + finalMsg)
        except BaseException as e:
            print(e)
        finally:
            return finalMsg

    def send_file(self, file_dir, tolists=tolist):
        theToList = tolists
        if theToList is None or theToList.__len__() == 0:
            theToList = self.tolist
        for user in theToList:
            fr = itchat.search_friends(user)
            for f in fr:
                itchat.send_file(file_dir, f.userName)

    def get_robots_key_by_friends(self, msg):
        if self.check_has_robot(msg):
            return self.friends_robots[msg.FromUserName]
        else:
            return self.init_friend_robot(msg, '李特尔飞什')

    def init_friend_robot(self, msg, robot='李特尔飞什'):
        self.friends_robots[msg.FromUserName] = self.robots[robot]['KEY']
        itchat.send_msg('我是机器人：' + robot, msg.FromUserName)
        return self.friends_robots[msg.FromUserName]

    def check_and_init_robot(self, msg):
        content = self.get_msg_content(msg)
        robots_name = '李特尔飞什'
        if content[0:4] == '机器人：' or content[0:4] == '机器人:':
            for key in self.robots:
                if content.find(key) > 1:
                    robots_name = key
                    break
            return self.init_friend_robot(msg, robots_name)

    def check_and_close_robot(self, msg):
        content = self.get_msg_content(msg)
        if content == '闭嘴机器人':
            try:
                del self.friends_robots[msg.FromUserName]
            finally:
                return

    def check_has_robot(self, msg):
        try:
            self.friends_robots[msg.FromUserName]
        except BaseException as e:
            return False
        return True

    def get_friend_name(self, friend_key_name, friends=friends):
        if friends is None:
            friends = itchat.get_friends()
        for f in friends:
            if f.UserName == friend_key_name:
                return f.RemarkName or f.NickName
        return friend_key_name

    def get_actual_name(self, msg):
        if hasattr(msg, 'ActualNickName'):
            return msg.ActualNickName
        else:
            return False

    def get_current_name(self):
        return self.friends[0].NickName

    def redirect_msg(self, finalMsg, tolists=tolist):
        theToList = tolists
        if theToList is None or theToList.__len__() == 0:
            theToList = self.tolist
        for user in theToList:
            fr = itchat.search_friends(user)
            for f in fr:
                itchat.send_msg(finalMsg, f.userName)


bot = wljbot()
@itchat.msg_register([PICTURE, RECORDING, ATTACHMENT, VIDEO], isFriendChat=True, isGroupChat=True,
                         isMpChat=False)
def muilt_msg(msg):
    print("mult")
    bot.get_files(msg)


@itchat.msg_register([PICTURE, RECORDING, ATTACHMENT, VIDEO], isFriendChat=True, isGroupChat=True,
                         isMpChat=False)
def text_msg(msg):
    print("text")
    bot.tuling_reply(msg)

bot.run()