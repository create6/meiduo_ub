from goods.models import GoodsChannel

def get_categories():
    #1,定义字典
    categories = {}

    #2,查询所有的频道组
    channels =  GoodsChannel.objects.order_by('group_id','sequence')

    #3,遍历频道组,组装数据
    for channel in channels:

        #3.1 取出组的编号
        group_id = channel.group_id

        #3.2组装好一个分类的字典
        if group_id not in categories:
            categories[group_id] = {"channels":[],"sub_cats":[]}

        #3.3添加一级分类到channels
        catetory = channel.category
        catetory_dict = {
            "id":catetory.id,
            "name":catetory.name,
            "url":channel.url
        }
        categories[group_id]["channels"].append(catetory_dict)

        #3.4添加二级分类三级分类
        for cat2 in catetory.subs.all():
            categories[group_id]["sub_cats"].append(cat2)
     #返回分类
    return categories