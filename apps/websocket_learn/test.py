#！coding:utf8
import tornado.ioloop
import tornado.web
import tornado.websocket


class ProStatus():
    connector = {}  # 记录当前连接的user

    def user_connect(self, user):
        if user not in self.connector:
            self.connector[user] = set()

    def user_remove(self, user):
        self.connector.remove(user)

    def trigger(self, message):
        ''' 向所有被记录的客户端推送最新内容 '''
        for user in self.connector:
            user.write_message(message)


class ReceiveHandler(tornado.web.RequestHandler):
    def get(self):
        msg = self.get_argument('msg', '')
        ProStatus().trigger(msg) # 接收到消息之后推送


class ConnectHandler(tornado.websocket.WebSocketHandler):
    def check_origin(self):
        '''重写同源检查 解决跨域问题'''
        return True

    def open(self):
        '''新的websocket连接后被调动'''
        ProStatus().user_connect(self) #用户连接后记录
        self.write_message('Welcome')

    def on_close(self):
        '''websocket连接关闭后被调用'''
        ProStatus().user_remove(self)  # 断开连接后remove

    def on_message(self, message):
        '''接收到客户端消息时被调用'''
        self.write_message('new message :' + message)


class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello world")


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r'/index', IndexHandler),
            (r'/ws', ConnectHandler),
            (r'/receive', ReceiveHandler)
        ]
        tornado.web.Application.__init__(self, handlers)


if __name__ == "__main__":
    app = Application()
    app.listen(8000)
    tornado.ioloop.IOLoop.current().start()