# coding:utf-8
import json

import datetime
from django.http import Http404
from django.http import HttpResponse
from django.shortcuts import render, redirect
from article.models import Article
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
        return item.content


def home(request):
    post_list = Article.objects.all()
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
