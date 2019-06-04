from django.conf import settings
from django.core.files.storage import Storage
"""
自定义文件存储类(官方文档-视图层-文件上传-自定义存储）:
1, 定义类继承自Storage
2, 必须保证参数能够初始化
3, 必须实现open,save方法

"""
class MyStorage(Storage):
    def __init__(self, base_url=None):
        if not base_url:
            base_url = settings.BASE_URL
        self.base_url = base_url

    def open(self, name, mode='rb'):
        """打开文件的时候调用"""
        pass

    def save(self, name, content, max_length=None):
        """保存文件的时候调用"""
        pass

    def exists(self, name):
        """上传的时候判断图片是否存在了"""
        pass

    def url(self, name):
        """返回图片的url地址"""
        return self.base_url + name