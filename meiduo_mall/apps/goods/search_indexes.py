import datetime
from haystack import indexes
from .models import SKU


class SKUIndex(indexes.SearchIndex, indexes.Indexable):
    #1,构建的索引字段,使用id,name,price作为模板
    text = indexes.CharField(document=True, use_template=True)
    # caption=indexes.CharField(model_attr='caption')
    # comments=indexes.IntegerField(model_attr='comments')

    #2,指定模型类
    def get_model(self):
        return SKU
    #3,提供数据集
    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.filter(is_launched=True)#只搜索上架的产品