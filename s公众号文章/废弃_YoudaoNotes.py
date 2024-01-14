#https://note.youdao.com/s/bhnffVZ0

#第一步构建conf/cookies.cfg
#
#https://blog.csdn.net/qq_43681877/article/details/126761272

#这里放弃了保存到有道云方案，而是网页文章保存到本地后通过脚本更新到github上。在github上，html也提供了解决方案看html超链接做了个转换，所以在有道云笔记引用没有问题
#所以这里放弃直接保存有道云的方案太难实现






import hashlib
import os
import queue
import shutil
import threading
import time
import uuid
import configparser
import requests

from ArticlesList import ArticlesList
from ParseArticles import ParseArticles


# sys.setdefaultencoding('utf8')

class YoudaoNote:
    def __init__(self):
        # 登录有道云笔记后存储在 Cookie 里的值
        conf = configparser.ConfigParser()
        conf.read('conf/cookies.cfg',encoding='utf-8')
        cstk = conf.get("youdao", "cstk")
        cookie = conf.get("youdao", "cookie")
        user_agent = conf.get("youdao", "user_agent")
        self.YNOTE_CSTK = cstk

        self.HEADERS = {
            'Accept-Encoding':
                'gzip, deflate, br',
            'User-Agent':
                user_agent,
            # 'Cookie': cookie + '{YNOTE_CSTK}'.
            #     format(YNOTE_CSTK=self.YNOTE_CSTK),  # use your own cookie
            'Cookie': cookie  ,   
            'Accept':
                'application/json, text/plain, */*',
            'Host':
                'note.youdao.com',
            'Origin':
                'https://note.youdao.com',
            'Referer':
                'https://note.youdao.com/web/',
            'Content-Type':
                'application/x-www-form-urlencoded;charset=UTF-8',
            "connection": "keep-alive"
        }

    # 获取某笔记本下所有的笔记本
    def getBooks(self, path):
        data = {'path': path, 'dirOnly': True, 'f': True, 'cstk': self.YNOTE_CSTK}
        url = 'https://note.youdao.com/yws/api/personal/file?method=listEntireByParentPath&cstk={CSTK}&keyfrom=web'.format(
            CSTK=self.YNOTE_CSTK)
        res = requests.post(url, data=data, headers=self.HEADERS)
        if res.status_code == 200:
            resJson = res.json()
            books = []
            for i in resJson:
                # _私密, _开头的笔记本认为是私密笔记, 跳过
                if i['fileEntry']['name'][0] != '_':
                    books.append({
                        'name': i['fileEntry']['name'],
                        'id': i['fileEntry']['id']
                    })
            print(len(books))
            return books
        else:
            exit('getBooks')

    # 获取所有的笔记本
    def getAllBooks(self, ):
        ids = queue.Queue()
        ids.put('/')
        books = []
        while not ids.empty():
            print(ids.queue)
            tempId = ids.get()
            tempBooks = self.getBooks(tempId)
            for book in tempBooks:
                if tempId == '/':
                    aId = tempId + book['id']
                else:
                    aId = tempId + '/' + book['id']
                ids.put(aId)
                books.append({
                    'name': book['name'],
                    'id': book['id']
                })
        print('allbooks')
        print(books)
        return books

    # 获取笔记本下的笔记
    def getAllNotes(self, book):
        url = 'https://note.youdao.com/yws/api/personal/file/{id}?all=true&cstk={CSTK}&f=true&isReverse=false&keyfrom=web&len=30&method=listPageByParentId&sort=1'.format(
            id=book['id'], CSTK=self.YNOTE_CSTK)
        res = requests.get(url, headers=self.HEADERS)
        if res.status_code == 200:
            resJson = res.json()
            notes = []
            for i in resJson['entries']:

                # 选出后缀名为md的文件
                if i['fileEntry']['name'][-2:] == 'md' and i['fileEntry']['name'][0] != '_':
                    notes.append({
                        'name':
                            i['fileEntry']['name'],
                        'id':
                            i['fileEntry']['id'],
                        'createTime':
                            i['fileEntry']['createTimeForSort'],
                        'modifyTime':
                            i['fileEntry']['modifyTimeForSort'],
                        'tag':
                            book['name']
                    })
            print(notes)
            return notes
        else:
            exit('getAllNotes')

    # 根据笔记信息获取笔记内容
    def getNoteDetail(self, note):
        url = "https://note.youdao.com/yws/api/personal/sync?method=download&keyfrom=web&cstk={CSTK}&sev=j1".format(
            CSTK=self.YNOTE_CSTK)
        data = {
            "fileId": note['id'],
            "version": -1,
            "read": "true",
            "cstk": self.YNOTE_CSTK
        }

        res = requests.get(url, headers=self.HEADERS, params=data)
        if res.status_code:
            resCon = res.content

            time = ''
            if note['modifyTime']:  # 优先选用修改时间
                time = self.parseTS(note['modifyTime'])
            else:
                time = self.parseTS(note['createTime'])

            detail = {
                'name': self.filterMark(note['name']),
                'time': time,
                'content': str(resCon),
                'tag': note['tag']
            }
            return detail
        else:
            exit('getNoteDetail')

    def createNote(self, content, title):
        url = "https://note.youdao.com/yws/api/personal/sync?method=push&keyfrom=web&cstk={CSTK}&sev=j1".format(
            CSTK=self.YNOTE_CSTK)
        fileId = "WEB" + uuid.uuid1().hex
        data = {
            "fileId": fileId,
            "parentId": "SVR168BF776AD9D44ABB8579527EF93CB26",
            "name": title,
            "domain": 1,
            "rootVersion": -1,
            "dir": "false",
            "sessionId": "",
            "bodyString": content.encode('utf-8'),
            "createTime": int(time.time()),
            "modifyTime": int(time.time()),
            "transactionId": fileId,
            "transactionTime": int(time.time())
        }

        res = requests.post(url, headers=self.HEADERS, data=data)
        if res.status_code == 200:
            print('Create note {} success!'.format(fileId))
            resCon = res.content
            print(resCon)
        else:
            print('Failed to create note {}!'.format(fileId))
            resCon = res.content
            print(resCon)
        return fileId

    def editNote(self, content, fileId):
        url = "https://note.youdao.com/yws/api/personal/sync?method=push&keyfrom=web&cstk={CSTK}&sev=j1".format(
            CSTK=self.YNOTE_CSTK)
        # content = '<section style="text-align: left;font-size: 14px;color: rgb(18, 17, 17);box-sizing: border-box;" powered-by="xiumi.us"><p style="margin: 0px;padding: 0px;box-sizing: border-box;"><strong style="box-sizing: border-box;">今日发音练习重点：</strong></p><p style="margin: 0px;padding: 0px;box-sizing: border-box;"><strong style="box-sizing: border-box;">1. one不要发成“完”或“忘”；</strong></p><p style="margin: 0px;padding: 0px;box-sizing: border-box;"><strong style="box-sizing: border-box;">2. plain和昨天早读的claim有共同点；</strong></p><p style="margin: 0px;padding: 0px;box-sizing: border-box;"><strong style="box-sizing: border-box;">3. tha</strong><span style="text-decoration: underline;color: rgb(255, 0, 0);"><strong style="box-sizing: border-box;">t y</strong></span><strong style="box-sizing: border-box;">ou\'re 两词弱读并连读同化。</strong></p></section>'

        data = {
            "fileId": fileId,
            "parentId": "SVR168BF776AD9D44ABB8579527EF93CB26",
            "domain": 1,
            "rootVersion": -1,
            "sessionId": "",
            "modifyTime": int(time.time()),
            "bodyString": content.encode('utf-8'),
            "transactionId": fileId,
            "transactionTime": int(time.time()),
            "tags": ""
        }

        res = requests.post(url, headers=self.HEADERS, data=data)
        if res.status_code:
            resCon = res.content
            print(resCon)

    def get_content_length(self, data):
        length = len(data.keys()) * 2 - 1
        total = ''.join(list(data.keys()) + list(data.values()))
        length += len(total)
        return length

    def writeMd(self, detail):
        print('写入: {name}'.format(name=detail['name']))
        with open('articles/' + detail['name'], 'w') as f:
            # f.write('---n')
            # f.write('title: {title}n'.format(title=detail['name'][:-3]))
            # f.write('date: {data}n'.format(data=detail['time']))
            # f.write('tags: {tag}n'.format(tag=detail['tag']))
            # f.write('---nnn')
            f.write(detail['content'])
            f.write('n')

    # 将10位时间戳转为 2017-06-29 10:00:00 的格式
    def parseTS(self, ts):
        timeArr = time.localtime(ts)
        return time.strftime("%Y-%m-%d %H:%M:%S", timeArr)

    # 过滤特殊字符, 移除原有后缀后重新添加.md
    def filterMark(self, s):
        # s = s.decode("utf8")
        # res = re.sub("[s+.!/_,$%^*(+"']+'[+——！，。？、~@#￥%……&*（）()]"+".decode("utf8"),"".decode("utf8"), s)
        res = s.replace(' ', '')
        return res[:-2] + '.md'

    # MD5 加密
    def md5(self, str):
        md5 = hashlib.md5()
        md5.update(str)
        return md5.hexdigest()

    # 退出程序
    def exit(self, why):
        print('{why} 出错了'.format(why=why))
        os.exit(0)

    def readHtmlContent(self, file_name):
        content = ""
        with open(file_name, "r", encoding="utf-8") as f:
            content = f.read()
            print(len(content))
        return content

    def start_download_notes(self):
        if os.path.exists('articles'):
            shutil.rmtree(r'articles')
        os.mkdir(r'articles')
        books = self.getAllBooks()
        for i in books:
            notes = self.getAllNotes(i)
            print(len(notes))
            for j in notes:
                detail = self.getNoteDetail(j)
                self.writeMd(detail)

        t = threading.Timer(432000, self.start)
        t.start()

    # 入口
    def run(self, files):
        if not files:
            files = os.listdir('articles')  # 获取指定路径下的文件
        names = []
        for file_name in files:  # 循环读取路径下的文件并筛选输出
            if os.path.splitext(file_name)[1] == ".md":  # 筛选csv文件
                print(file_name)
                names.append(file_name)
                content = self.readHtmlContent('articles/' + file_name)
                print("Load content from html file {}.".format('articles/' + file_name))
                note_id = self.createNote(content, file_name)
                print(note_id)
                time.sleep(10)


if __name__ == '__main__':
    # debug_get_content_list()
    articles_ins = ArticlesList('波段之门')
    print("Start from date {}:".format(articles_ins.cut_date))
    list_file = articles_ins.get_articles_list(articles_ins.cut_date)
    parser = ParseArticles(list_file)
    file_names = parser.run()
    # file_names = ['2022Y3W_20220117-20220123.md']
    youdao = YoudaoNote()
    youdao.run(file_names)
