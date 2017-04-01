# -*- coding:utf-8 -*-

from __future__ import unicode_literals

from django.core.urlresolvers import reverse

from django.db import models
from django.utils.translation import ugettext_lazy as _


# Create your models here.


class Article(models.Model):
    title = models.CharField(max_length=100)  # 博客题目
    category = models.CharField(max_length=50, blank=True)  # 博客标签
    date_time = models.DateTimeField(auto_now_add=True)  # 博客日期
    content = models.TextField(blank=True, null=True)  # 博客文章正文

    def get_absolute_url(self):
        path = reverse('detail', kwargs={'id': self.id})
        return "http://0.0.0.0:8000%s" % path


    def __str__(self):
        return self.title

    class Meta:  # 按时间下降排序
        ordering = ['-date_time']
        verbose_name = _(u'文章列表')
        verbose_name_plural = _(u'文章列表')


