# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class ProjectConfd(models.Model):
    project_name = models.CharField(max_length=40, verbose_name=u'项目名称')
    project_url = models.CharField(max_length=40, verbose_name=u'项目目录')


class VhostsConfd(models.Model):
    STATUS = (
        (0, 'UP'),
        (1, 'Down'),
    )

    project_name = models.ForeignKey(ProjectConfd, verbose_name=u'项目名称', blank=True, null=True, on_delete=models.SET_NULL)
    vhosts_key = models.CharField(max_length=40, verbose_name=u'子项目路径', unique=True)
    vhosts_value  = models.CharField(max_length=40, verbose_name=u'程序目录')
    vhosts_status = models.IntegerField(choices=STATUS, default=0, verbose_name=u'工单状态')


