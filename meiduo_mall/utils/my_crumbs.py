from goods.models import SKU,GoodsCategory

#1获取面包屑的分类
def get_crumbs(sku_id):
    sku=SKU.objects.get(id=sku_id)
    return GoodsCategory.objects.get(id=sku.category_id)