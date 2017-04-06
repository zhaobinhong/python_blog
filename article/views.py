# coding:utf-8
import json

import datetime
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django import forms
from django.http import Http404
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, render_to_response
from django.template import RequestContext

from article.models import Article, User
from django.contrib.syndication.views import Feed


# Create your views here.


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


# 表单

class UserForm(forms.Form):
    username = forms.CharField(label='用户名', max_length=100)
    password = forms.CharField(label='密码', widget=forms.PasswordInput())


# 注册
def regist(req):
    if req.method == "POST":
        uf = UserForm(req.POST)
        print uf
        if uf.is_valid():
            # 获得表单数据
            username = uf.cleaned_data['username']
            password = uf.cleaned_data['password']
            print username
            # 添加到数据库
            User.objects.create(username=username, password=password)
            return HttpResponse('<p>注册成功</p><br/><a href="/online/login/">到登录</a>')
    else:
        uf = UserForm()
    return render_to_response('regist.html', {'uf': uf})


# 登陆
def login(req):
    if req.method == 'POST':
        uf = UserForm(req.POST)
        if uf.is_valid():
            # 获取表单用户密码
            username = uf.cleaned_data['username']
            password = uf.cleaned_data['password']
            # 获取的表单数据与数据库进行比较
            user = User.objects.filter(username__exact=username, password__exact=password)
            if user:
                # 比较成功，跳转index
                response = HttpResponseRedirect('/?username=' + username)
                # 将username写入浏览器cookie,失效时间为3600
                response.set_cookie('username', username, 3600)
                return response
            else:
                # 比较失败，还在login
                return HttpResponseRedirect('/online/login/')
    else:
        uf = UserForm()
    return render_to_response('login.html', {'uf': uf})


# 登陆成功
def index(req):
    username = req.COOKIES.get('username', '')
    return render_to_response('base.html', {'username': username})


# 退出
def logout(req):
    response = render_to_response('base.html', {'username': '请登录'})
    # 清理cookie里保存username
    response.delete_cookie('username')
    return response
