from django import http
from django.core.paginator import Paginator
from django.shortcuts import render
from django.views import View
from goods.models import GoodsCategory, SKU
from meiduo_mall.utils.My_categoery import get_categories
from meiduo_mall.utils.my_crumbs import get_crumbs

#分类表list
class SkuListView(View):
    def get(self,request,category_id,page_num):
        #1 获取分类信息
        categories=get_categories()
        #1.2排序参数
        sort=request.GET.get("sort","default")
        #1.3根据sort设置排序方式
        if sort =="price" :
            sort_field="-price"
        elif sort=="hot":
            sort_field="-sales"
        else:
            sort_field="-create_time"
        #2 获取分类对象
        category=GoodsCategory.objects.get(id=category_id)
        # 3,分页查询
        skus = SKU.objects.filter(category_id=category_id).order_by(sort_field)
        paginator = Paginator(object_list=skus, per_page=5)  # 创建分类对象,每页5条
        page = paginator.page(page_num)  # 获取page_num页
        skus_list = page.object_list  # 获取page_num中的所有的对象
        current_page = page.number  # 当前页
        total_page = paginator.num_pages  #
        # 总页数

        #拼接数据，返回响应
        context = {
            "categories": categories,
            "category": category,
            "skus_list": skus_list,
            "current_page": current_page,
            "total_page": total_page,
            "sort": sort
        }

        return render(request,'list.html',context=context)

#热销
class HotSkuView(View):
    def get(self,request,category_id):
        #1,根据销量获取两个sku对象
        skus=SKU.objects.filter(category_id=category_id).order_by("-sales")[:3]
        #2,拼接数据
        hot_sku_list=[]
        for sku in skus:
            sku_dict={
                "id":sku.id,
                "default_image_url":sku.default_image_url.url,
                "name":sku.name,
                "price":sku.price
            }
            hot_sku_list.append(sku_dict)
        #3,返回响应
        return http.JsonResponse({"hot_sku_list":hot_sku_list})

#详情页
class SKUDetailView(View):
    def get(self,request,sku_id):

        #1,获取分类数据
        categories = get_categories()

        #2,获取面包屑数据
        category = get_crumbs(sku_id)
        #3,查询商品sku对象
        sku=SKU.objects.get(id=sku_id)

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

        #携带数据渲染页面
        context = {
            "categories":categories,
            "category":category,
            "sku": sku,
            "specs": goods_specs
        }

        return render(request,'detail.html',context=context)

#分类访问量类视图
class GoodsVisitView(View):

    pass
