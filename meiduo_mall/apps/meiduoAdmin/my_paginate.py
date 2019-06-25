from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

class MyPageNumberPagination(PageNumberPagination):
    #1,每页的默认数量
    page_size = 2

    #2,每页最大数量
    max_page_size = 10

    #3,指定每页大小
    page_size_query_param = "pagesize"

    #4,重写系统方法,返回指定的格式数据
    def get_paginated_response(self, data):
        return Response({
            "lists":data,
            "page":self.page.number,
            "pages":self.page.paginator.num_pages
        })