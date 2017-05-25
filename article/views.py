# coding:utf-8
import json
import os
import re
import urllib
import urllib2

import datetime
from django.contrib.syndication.views import Feed
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import Http404
from django.http import HttpResponse
from django.shortcuts import render, redirect

from article.models import Article

# Create your views here.

FILEURI = '/vagrant/myblog/file/'


class RSSFeed(Feed):
    title = "RSS feed - article"
    link = "feeds/posts/"
    description = "RSS feed - blog posts"

    def items(self):
        return Article.objects.order_by('-date_time')

    def item_title(self, item):
        return item.title

    # def item_pubdate(self, item):
    #     return item.add_date

    def item_description(self, item):
        return item.conte


def home(request):
    post_list = Article.objects.all()
    # 分页
    paginator = Paginator(post_list, 2)
    page = request.GET.get('page')
    try:
        post_list = paginator.page(page)
    except PageNotAnInteger:
        post_list = paginator.page(1)
    except EmptyPage:
        post_list = paginator.page(paginator.num_pages)
    return render(request, 'home.html', {'post_list': post_list})


def detail(request, id):
    # posts = Article.objects.all().filter(id=my_args)

    # if len(posts):
    #     for post in posts:
    #         # print post.id, post.title, post.date_time, post.category, post.content
    #
    #         str = ("title = %s, category = %s, date_time = %s, content = %s"
    #                % (post.title, post.category, post.date_time, post.content))
    #         return HttpResponse(str)
    # else:
    #     return HttpResponse("没有数据")

    try:
        post = Article.objects.all().get(id=str(id))
    except Article.DoesNotExist:
        raise Http404
    return render(request, 'post.html', {'post': post})


def test(request):
    return render(request, 'template.html', {'current_time': datetime.datetime.now()})


def archives(request):
    try:
        post_list = Article.objects.all()
    except Article.DoesNotExist:
        raise Http404
    return render(request, 'archives.html', {'post_list': post_list, 'error': False})


def about_me(request):
    return render(request, 'aboutme.html')


def search_tag(request, tag):
    try:
        post_list = Article.objects.filter(category__iexact=tag)  # contains
    except Article.DoesNotExist:
        raise Http404
    return render(request, 'tag.html', {'post_list': post_list, 'error': False})


def blog_search(request):
    if 's' in request.GET:
        s = request.GET['s']
        if not s:
            return render(request, 'home.html')
        else:
            post_list = Article.objects.filter(title__icontains=s)
            if len(post_list) == 0:
                return render(request, 'archives.html', {'post_list': post_list,
                                                         'error': True})
            else:
                return render(request, 'archives.html', {'post_list': post_list,
                                                         'error': False})
    return redirect('/')


def write(request):
    date = datetime.datetime.now()
    return render(request, 'write.html', {"date1": date})


#
# class writeSqlViewSet(viewsets.ModelViewSet):
#     '''
#     存文章接口
#     '''
#     queryset = Article.objects.all()
#     serializer_class = ArticleSerializer
#     permission_classes = (IsAuthenticated,)




def mgmt_files(request):  # 列出树形目录，上传文件页面
    if request.method == 'POST':
        # path_root = "/file/"  # 上传文件的主目录
        myFile = request.FILES.get("file", None)  # 获取上传的文件，如果没有文件，则默认为None
        if not myFile:
            dstatus = "请选择需要上传的文件!"
        else:
            # os.path.abspath(path)：绝对路径
            # os.path.curdir  当前路径
            path_ostype = os.path.abspath('/vagrant/myblog/article/file/')
            path_dst_file = os.path.join(os.path.curdir + '/file/', myFile.name)
            # print path_dst_file
            if os.path.isfile(path_dst_file):
                dstatus = {"status": "文件已存在，请先删除再上传", "fileName": myFile.name}
            else:
                destination = open(path_dst_file, 'wb+')  # 打开特定的文件进行二进制的写操作
                for chunk in myFile.chunks():  # 分块写入文件
                    destination.write(chunk)
                destination.close()
                # print myFile.name
                dstatus = {"status": "上传成功", "fileName": myFile.name}
        return HttpResponse(json.dumps(dstatus))
    else:

        return render(request, 'mgmt_files.html')


def mgmt_file_download(request, *args, **kwargs):  # 提供文件下载页面

    if request.method == 'GET':
        a = os.listdir(FILEURI)
        # print a
    return HttpResponse(str(a))


def rm(request):
    if request.method == 'GET':
        uri = request.get_full_path()
        fileName = result = re.split('\?', uri)
        # print fileName[1]
        os.remove(FILEURI + fileName[1])

        return HttpResponse('已删除')


def download(request):
    if request.method == 'GET':
        uri = request.get_full_path()
        fileName = result = re.split('\?', uri)
        url = "http://10.7.7.47:8080" + uri

        return HttpResponse('下载完成')
