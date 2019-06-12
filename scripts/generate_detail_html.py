#! /usr/bin/env python
# #1,将scripts添加到导包路径
import sys
sys.path.insert(0, '../')

#2,加载dev配置文件
import os
if not os.getenv('DJANGO_SETTINGS_MODULE'):
    os.environ['DJANGO_SETTINGS_MODULE'] = 'meiduo_mall.settings.dev'

#3,让加载的环境变量dev生效
import django
django.setup()

#4,导入用到的包
from django.template import loader
from meiduo_mall.utils.My_categoery import get_categories
from meiduo_mall.utils.my_crumbs import get_crumbs
from goods.models import SKU
from django.conf import settings

def generate_static_detail_html(sku_id):
    # 1,获取分类数据
    categories = get_categories()

    # 2,获取面包屑数据
    category = get_crumbs(sku_id)

    # 3,查询商品sku对象
    sku = SKU.objects.get(id=sku_id)

    # 4,商品sku规格信息
    # 构建当前商品的规格键
    sku_specs = sku.specs.order_by('spec_id')
    sku_key = []
    for spec in sku_specs:
        sku_key.append(spec.option.id)
    # 获取当前商品的所有SKU
    skus = sku.spu.sku_set.all()
    # 构建不同规格参数（选项）的sku字典
    spec_sku_map = {}
    for s in skus:
        # 获取sku的规格参数
        s_specs = s.specs.order_by('spec_id')
        # 用于形成规格参数-sku字典的键
        key = []
        for spec in s_specs:
            key.append(spec.option.id)
        # 向规格参数-sku字典添加记录
        spec_sku_map[tuple(key)] = s.id
    # 获取当前商品的规格信息
    goods_specs = sku.spu.specs.order_by('id')
    # 若当前sku的规格信息不完整，则不再继续
    if len(sku_key) < len(goods_specs):
        return
    for index, spec in enumerate(goods_specs):
        # 复制当前sku的规格键
        key = sku_key[:]
        # 该规格的选项
        spec_options = spec.options.all()
        for option in spec_options:
            # 在规格参数sku字典中查找符合当前规格的sku
            key[index] = option.id
            option.sku_id = spec_sku_map.get(tuple(key))
        spec.spec_options = spec_options

    # 携带数据渲染页面
    context = {
        "categories": categories,
        "category": category,
        "sku": sku,
        "specs": goods_specs
    }

    #1,获取详情页模板
    template = loader.get_template('detail.html')
    html_text = template.render(context)

    #2,获取文件路径
    file_path = os.path.join(settings.STATICFILES_DIRS[0], 'detail/'+str(sku_id)+'.html')

    #3,将数据写入到路径中
    with open(file_path, 'w',encoding='utf-8') as f:
        f.write(html_text)





if __name__ == '__main__':
    skus = SKU.objects.all()
    for sku in skus:
        print(sku.id)
        generate_static_detail_html(sku.id)