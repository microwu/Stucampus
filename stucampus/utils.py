# -*- coding:utf-8 -*-
import json
import urllib2
import arrow

from django.http import HttpResponse
from django.conf import settings



def render_json(context, **response_kwargs):
    data = json.dumps(context)
    response_kwargs['content_type'] = 'application/json'
    return HttpResponse(data, **response_kwargs)


def spec_json(status='Error', messages=None):
    if not messages:
        messages = []
    elif not isinstance(messages, (dict, list, tuple)):
        messages = [messages]
    data = {'status': status, 'messages': messages}
    return render_json(data)


def get_client_ip(request):
    '''Get the ip of client'''
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


class DuoShuo(object):
    """
        @author:jimczj@gmail.com
        docstring for Duoshuo http://dev.duoshuo.com/docs
    """
    short_name=settings.DUOSHUO_SHORT_NAME
    list_posts_url="http://api.duoshuo.com/threads/listPosts.json?short_name="+short_name
    list_top_threads_url="http://api.duoshuo.com/sites/listTopThreads.json?short_name="+short_name
    comments_num_url="http://api.duoshuo.com/threads/counts.json?short_name="+short_name
    user_message_url="http://api.duoshuo.com/users/profile.json?user_id="
    comments_url="http://api.duoshuo.com/posts/create.json"
    article_sync_url = "http://api.duoshuo.com/threads/sync.json"
    list_visitors_url="http://"+short_name+".duoshuo.com/api/sites/listVisitors.json?num_items="
    recent_comment_url="http://"+short_name+".duoshuo.com/api/sites/listRecentPosts.json"
      
    
    def __init__(self):
        pass

    @staticmethod    
    def getJson(url):
        try:
            response=urllib2.urlopen(url)
            response_content=response.read()
            response_json=json.loads(response_content)
            return response_json
        except Exception, e:
            print str(e)
            return False
            
    @staticmethod
    def post(url, data): 
        try: 
            req = urllib2.Request(url)  
            data = urllib.urlencode(data)  
            #enable cookie  
            opener = urllib2.build_opener(urllib2.HTTPCookieProcessor())  
            response = opener.open(req, data) 
            response_json=json.loads(response.read()) 
            return response_json
        except Exception, e:
            print str(e)
            return False

    @classmethod
    def getListPosts(cls,id,page=1,limit=8,order='desc'):
        '''
            文章页返回的
            获取文章评论
            详细看 http://dev.duoshuo.com/docs/54460b82f42e54ec03e50082
            http://api.duoshuo.com/threads/listPosts.json?order=asc&thread_key=article1&short_name=official&page=1&limit=10
        '''
        thread_key="article-comments-"+str(id)
        url=cls.list_posts_url+"&order="+order+"&thread_key="+thread_key+"&page="+str(page)+"&limit="+str(limit)
        json=cls.getJson(url)
        if json == False:
            return json
        parent_posts=json['parentPosts']
        comments=[]
        for parent_post in parent_posts:
            comment={}
            parent_posts_value= parent_posts[parent_post]
            comment["author"]=parent_posts_value["author"]
            '''
                因为在返回数据中有None
                而如果直接传输None的话
                会导致读取不到头像
                并且拖慢加载速度
                因此加了以下几行
                Corrected by GearLiu<gearliu155@gmail.com>
            '''
            comment['author']['name']=cls.handleUndefinedName(comment["author"]["name"])
            comment["author"]["url"]=cls.handleNoneUrl(comment["author"]["url"])
            comment["author"]["avatar_url"]=cls.handleNoneAvatarUrl(comment["author"]["avatar_url"])  #无头像时用多说默认头像
            comment["message"]=parent_posts_value["message"]
            comment["created_at"]=cls.handleDate(parent_posts_value["created_at"])
            comment["likes"]=parent_posts_value["likes"]
            comments.append(comment)
        comments = sorted(comments, cmp=lambda x,y:cmp(x["likes"],y["likes"]),reverse=True)
        return comments

    @classmethod
    def getListTopThreads(cls,range="all"):
        '''
            返回热评文章
        '''
        url=cls.list_top_threads_url+"&range="+range
        return cls.getJson(url)

    @classmethod
    def getCommentsAndLikesNum(cls,id):
        '''
            返回文章评论数,点赞数
        '''
        threads="article-comments-"+str(id)
        url=cls.comments_num_url+"&threads="+threads
        comments_num_json=cls.getJson(url)
        if comments_num_json == False:
            return comments_num_json
        threads_json=comments_num_json.get("response").get(threads)
        comments_and_likes_num={}
        comments_and_likes_num["likes"]=threads_json.get("likes")
        comments_and_likes_num["comments"]=threads_json.get("comments")
        return comments_and_likes_num

    @classmethod
    def appendNumToArticle(cls,article):
        '''
            给文章添加评论数和点赞数
        '''
        
        try:
            comments_and_likes_num=cls.getCommentsAndLikesNum(article.id)
            article.comments=comments_and_likes_num['comments']
            article.likes=comments_and_likes_num['likes']
        except Exception,e:
            print str(e)
        finally:
            return article

    @classmethod
    def appendNumToArticles(cls,articles):
        '''
            给文章列表添加评论数和点赞数
        '''
        try:
            for article in articles:
                comments_and_likes_num=cls.getCommentsAndLikesNum(article.id)
                article.comments=comments_and_likes_num['comments']
                article.likes=comments_and_likes_num['likes']
        except Exception,e:
            print str(e)
        finally:
            return articles

   


    @classmethod
    def getUserMessage(cls,userId):
        '''
            返回用户信息
        '''
        url=cls.user_message_url+str(userId)
        user_message_json=cls.getJson(url)
        return user_message_json

    # @classmethod
    # def sync_comment(cls,posts):
    #     '''
    #         传入评论对象,同步到多说,未测试
    #     '''
    #     data = urllib.urlencode({
    #      'data' : posts,
    #     })
    #     response_json = cls.post(cls.comments_url,posts)
    #     return response_json

    # @classmethod
    # def sync_article(cls,article):
    #     '''
    #         传入article对象,同步article到多说,未测试
    #     '''
    #     data = {
    #         'short_name' : cls.short_name,
    #         'secret ':cls.secret,
    #         'threads':["article-comments-"+str(article.id)],
    #         'thread_key' : article.id,
    #         'url' : article.url,
    #         'title':article.title,
    #         'content':article.content,
    #     }
    
    #     response_json = post(cls.article_sync_url,data)
    #     return response_json

    @classmethod
    def getListVisitors(cls,num_items=10):
        '''
            首页返回的最近访客
        '''
        url=cls.list_visitors_url+str(num_items)
        json=cls.getJson(url)
        if json == False:
            return json
        visitors_json=json["response"]
        visitors=[]
        for json in visitors_json:
            visitor={}
            visitor['user_id']=json['user_id']
            visitor['name']=json['name']
            visitor['url']=cls.handleNoneUrl(json['url'])
            visitor['avatar_url']=cls.handleNoneAvatarUrl(json['avatar_url'] )
            visitor['visited_at']=cls.handleDate(json['visited_at'])
            visitors.append(visitor)
        return visitors

    @classmethod
    def getRecentComment(cls):
        '''
            首页返回的最近评论
        '''
        url=cls.recent_comment_url
        json=cls.getJson(url)
        if json == False:
            return json
        comments_json=json["response"]
        comments=[]
        for json in comments_json:
            comment={}
            comment["comment_author_url"]=cls.handleNoneUrl(json["author"]['url'])          
            comment["comment_author_name"]=cls.handleUndefinedName(json["author"]['name'])
            comment["comment_author_avatar_url"]=cls.handleNoneAvatarUrl(json["author"]['avatar_url']) 
            comment["comment_created_at"]=cls.handleDate(json['created_at'])
            comment["comment_content"]=json["message"]
            comment["article_title"]=json["thread"]['title']
            comment["article_url"]=cls.handleNoneUrl(json["thread"]['url'])
            comments.append(comment)
        return comments

    @staticmethod
    def handleNoneUrl(url):
        if url is None:
            return "javascript:void(0)"
        return url

    @staticmethod
    def handleNoneAvatarUrl(url):
        if url is None:
            return "http://static.duoshuo.com/images/noavatar_default.png"
        return url

    @staticmethod
    def handleDate(date):
        '''
            返回距离现在的时间间隔
        '''
        return arrow.get(date).humanize(locale='zh_CN')
        

    @staticmethod
    def handleUndefinedName(name):
        if name == u"undefined":
            return u"匿名者"
        return name
    








#print DuoShuo.getListPosts(254)
#print DuoShuo.getListVisitors()[0]
#print DuoShuo.getRecentComment()[0]
#print DuoShuo.getCommentsAndLikesNum(254)
#print DuoShuo.getListTopThreads()
#print DuoShuo.getUserMessage(254)






        



