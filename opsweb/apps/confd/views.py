# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from pure_pagination.mixins import PaginationMixin
from django.views.generic import View, TemplateView, ListView, DetailView
from confd.models import ProjectConfd, VhostsConfd
from confd.forms import ProjectForm, VhostForm
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from utils.etcd_api import create_dir,delete_dir, create_vhost, delete_vhost
from django.db.models import Q
from django.http import HttpResponse, JsonResponse, QueryDict, Http404

# Create your views here.


class CreateProjectView(LoginRequiredMixin, TemplateView):
    '''
      创建一个空白项目目录
    '''
    template_name = 'confd/apply_project.html'

    def get_context_data(self, **kwargs):
        context = super(CreateProjectView, self).get_context_data(**kwargs)
        context['projects'] = ProjectConfd.objects.values('id', 'project_name')
        return context

    def post(self, request):
        webdata = request.POST.dict()
        webdata['project_url'] = webdata['project_url'].strip()

        # 如果没选择上级项目,直接创建空白项目
        if webdata['superior_project_name'] == '----\u8bf7\u9009\u62e9----':
            webdata['project_url'] = '/' + webdata['project_url']
            if projects_form(webdata, request):
               return HttpResponseRedirect(reverse('confd:project_list'))
        # 如果有选择上级项目,进行项目目录拼接创建项目
        else:
            pk = webdata.get('superior_project_name')
            project_url = ProjectConfd.objects.filter(pk=pk).values('project_url')[0]
            webdata['project_url'] = project_url['project_url'] + '/' + webdata['project_url']
            if projects_form(webdata, request):
                return HttpResponseRedirect(reverse('confd:project_list'))


def projects_form(webdata, request):
    forms = ProjectForm(webdata)
    if forms.is_valid():
        try:
            if create_dir(webdata['project_url']):
                forms.save()
                return HttpResponseRedirect(reverse('confd:project_list'))
            else:
                return render(request, 'confd/apply_project.html', {'forms': forms, 'errmsg': '项目创建失败'})
        except:
            return render(request, 'confd/apply_project.html', {'forms': forms, 'errmsg': '项目创建失败'})


class ProjectListView(LoginRequiredMixin, PaginationMixin, ListView):
    '''
      项目列表，删除项目
    '''
    model = ProjectConfd
    template_name = 'confd/project_list.html'
    context_object_name = "project_list"
    paginate_by = 10
    keyword = ''

    def get_queryset(self):
        queryset = super(ProjectListView, self).get_queryset()
        self.keyword = self.request.GET.get('keyword', '')
        if self.keyword:
            queryset = queryset.filter(Q(project_name__icontains = self.keyword)|
                                       Q(project_url__icontains = self.keyword))
        return queryset

    def get_context_data(self, **kwargs):
        context = super(ProjectListView, self).get_context_data(**kwargs)
        context['keyword'] = self.keyword
        return context

    def delete(self, request, *args, **kwargs):
        try:
            data = QueryDict(request.body)
            pk = data.get('id')
            project_url = ProjectConfd.objects.filter(pk=pk).values('project_url')[0]
            if delete_dir(project_url['project_url']):
                project = ProjectConfd.objects.filter(pk=pk).delete()
                ret = {'code': 0, 'result': '删除成功！'}
            else:
                ret = {'code': 1, 'result': '该项目里面有子项目！'}
        except:
            ret = {'code': 1, 'result': '该项目里面有子项目！'}
        return JsonResponse(ret, safe=True)


class CreateVhostView(LoginRequiredMixin, TemplateView):
    '''
     添加虚拟主机
    '''
    template_name = 'confd/apply_vhost.html'

    def get_context_data(self, **kwargs):
        context = super(CreateVhostView, self).get_context_data(**kwargs)
        context['projects'] = ProjectConfd.objects.values('id', 'project_name')
        return context

    def post(self, request):
        webdata = request.POST.dict()
        project_name = webdata.get('project_name')
        project = ProjectConfd.objects.filter(pk=project_name).values('project_url')[0]
        webdata['vhosts_key'] = project['project_url'] + '/' + webdata['vhosts_key']
        forms = VhostForm(webdata)
        if forms.is_valid():
            try:
                if create_vhost(webdata['vhosts_key'], webdata['vhosts_value']):
                    forms.save()
                    return HttpResponseRedirect(reverse('confd:vhost_list'))
                else:
                    ret = {'code': 1, 'result': '添加失败！'}
            except:
                ret = {'code': 1, 'result': '添加失败！'}
        else:
            ret = {'code': 1, 'result': '添加失败！'}
        return JsonResponse(ret, safe=True)


class VhostListView(LoginRequiredMixin, PaginationMixin, ListView):

    '''
      虚拟主机列表,信息修改
    '''
    model = VhostsConfd
    template_name = 'confd/vhost_list.html'
    context_object_name = "vhosts_list"
    paginate_by = 10
    keyword = ''

    def get_queryset(self):
        queryset = super(VhostListView, self).get_queryset()
        self.keyword = self.request.GET.get('keyword', '')
        if self.keyword:
            queryset = queryset.filter(Q(vhosts_key__icontains = self.keyword)|
                                       Q(vhosts_value__icontains = self.keyword))
        return queryset

    def get_context_data(self, **kwargs):
        context = super(VhostListView, self).get_context_data(**kwargs)
        context['keyword'] = self.keyword
        context['projects'] = ProjectConfd.objects.all()
        return context

    def post(self, request):
        webdata = request.POST.dict()
        vhosts_object = VhostsConfd.objects.get(pk=webdata['id'])
        try:
            if create_vhost(webdata['vhosts_key'],webdata['vhosts_value']):
                vhosts_object.vhosts_value = webdata['vhosts_value']
                vhosts_object.save()
                return HttpResponseRedirect(reverse('confd:vhost_list'))
            else:
                ret = {'code': 1, 'result': '修改失败！'}
        except:
            ret = {'code': 1, 'result': '修改失败！'}
        return JsonResponse(ret, safe=True)

    def put(self, request):
        data = QueryDict(request.body)
        pk = data.get('id')
        status = data.get('status')
        vhosts_object = VhostsConfd.objects.get(pk=pk)
        if VhostsConfd.objects.filter(pk=pk, vhosts_key__icontains = 'upstream'):
            if status == '0':
                vhosts_object.vhosts_value = vhosts_object.vhosts_value + ' down'
                vhosts_object.vhosts_status = 1
                create_vhost(vhosts_object.vhosts_key, vhosts_object.vhosts_value)
                vhosts_object.save()
                ret = {'code': 0, 'result': '修改成功！'}

            elif status == '1':
                value = vhosts_object.vhosts_value.split(' ')[0]
                vhosts_object.vhosts_status = 0
                vhosts_object.vhosts_value = value
                create_vhost(vhosts_object.vhosts_key, value)
                vhosts_object.save()
                ret = {'code': 0, 'result': '修改成功！'}

            else:
                ret = {'code': 1, 'result': '修改失败！'}
        else:
            ret = {'code': 1, 'result': '该字段没有此功能！'}
        return JsonResponse(ret, safe=True)

    def delete(self, request, *args, **kwargs):
        data = QueryDict(request.body)
        pk = data.get('id')
        vhosts_key = VhostsConfd.objects.filter(pk=pk).values('vhosts_key')[0]
        try:
            if delete_vhost(vhosts_key['vhosts_key']):
                vhost = VhostsConfd.objects.filter(pk=pk).delete()
                ret = {'code': 0, 'result': '删除成功！'}
            else:
                ret = {'code': 1, 'result': '该项目里面有子项目！'}
        except:
            ret = {'code': 1, 'result': '该项目里面有子项目！'}

        return JsonResponse(ret, safe=True)


class VhostDetailView(LoginRequiredMixin, DetailView):
    '''
         虚拟主机配置详情
    '''
    template_name = 'confd/vhost_detail.html'
    model = VhostsConfd
    context_object_name = 'vhost_detail'


