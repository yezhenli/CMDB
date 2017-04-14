#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
@Time: 2017/2/14

@Author: Yezl
'''
from django.utils.safestring import mark_safe

class PageInfo:

    def __init__(self,current_page,all_count,per_item=5):
        '''
        :param current_page: 当前页
        :param all_count: 总数据条目
        :param per_item: 每页显示条目
        :return:
        '''
        self.CurrentPage = current_page
        self.AllCount = all_count
        self.PerItem = per_item

    @property
    def start(self):
        '''
        :return: 返回页面起始
        '''
        return (self.CurrentPage-1)*self.PerItem

    @property
    def end(self):
        '''
        :return:返回页面结束
        '''
        return self.CurrentPage*self.PerItem

    @property
    def all_page_count(self):
        '''
        :return: 返回总页面数
        '''
        temp = divmod(self.AllCount,self.PerItem)
        if temp[1] == 0:
            all_pages_count = temp[0]
        else:
            all_pages_count = temp[0] + 1
        return all_pages_count

def Pager(page,all_page_count):
    '''
    HTML分页
    :param page: current page
    :param all_page_count: the number of pages
    :return:
    '''

    # 页面标签列表
    page_html = []
    # 首页
    first_html = "<a href='/assets/asset_list/'>首页</a>"
    # 如果上一页小于首页不跳转
    if page <= 1:
        pre_html = "<a href='#'>上一页</a>"
    else:
        pre_html = "<a href='/assets/asset_list/%d'>上一页</a>"%(page-1)
    page_html.append(first_html)
    page_html.append(pre_html)
    if all_page_count <= 11:
        start = 0
        end = all_page_count
    else:
        if page <= 6:
            start = 0
            end = 11
        else:
            if page + 5 >= all_page_count:
                start = page - 6
                end = all_page_count
            else:
                start = page - 6
                end =  page + 5
    # 获取每页的条目数据
    for i in range(start,end):
        if page == i+1:
           a_html = "<a style='border:none;' href='/assets/asset_list/%s'>%s</a>"%(i+1,i+1)
        else:
            a_html = "<a href='/assets/asset_list/%s'>%s</a>"%(i+1,i+1)
        page_html.append(a_html)
    # 如果下一页超过总页数，不跳转
    if page >= all_page_count:
        next_html = "<a href=''>下一页</a>"
    else:
        next_html = "<a href='/assets/asset_list/%d'>下一页</a>"%(page+1)
    page_html.append(next_html)
    # 尾页
    end_html = "<a href='/assets/asset_list/%s'>尾页</a>"%(all_page_count,)
    page_html.append(end_html)

    # 将HTML页面标签拼接成字符串，并以HTML页面形式返回
    string_html = mark_safe(''.join(page_html))
    # 返回字符串形式的html页面
    return string_html