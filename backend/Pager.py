#!/usr/bin/env python
#coding:utf-8
from django.core.paginator import Paginator
from django.core.paginator import PageNotAnInteger
from django.core.paginator import EmptyPage

class JuncheePaginator(Paginator):
    def __init__(self, object_list, per_page, range_num=5, orphans=0, allow_empty_first_page=True):
        '''
        :param range_num: 左右各显示多少标签
        '''
        Paginator.__init__(self, object_list, per_page, orphans, allow_empty_first_page)
        self.range_num = range_num

    def page(self, number):
        self.page_num = number
        return super(JuncheePaginator,self).page(number)

    def _page_range_ext(self):
        num_count = 2 * self.range_num + 1
        if self.num_pages <= num_count:
            return range(1, self.num_pages+1)
        num_list = []
        num_list.append(self.page_num)
        for i in range(1, self.range_num+1):
            if self.page_num - i <= 0:
                num_list.append(self.page_num + num_count -i)
            else:
                num_list.append(self.page_num - i)

            if self.page_num + i <= self.num_pages:
                num_list.append(self.page_num + i)
            else:
                num_list.append(self.page_num + i - num_count)
        num_list.sort()
        return num_list
    page_range_ext = property(_page_range_ext)