from django.db import models
from meiduo_mall.utils.models import BaseModel
from orders.models import OrderInfo

#1,关联美多和支付宝编号
class Payment(BaseModel):
    order = models.ForeignKey(OrderInfo, on_delete=models.CASCADE, verbose_name="美多订单号")
    trade_id = models.CharField(max_length=100, unique=True, null=True, blank=True, verbose_name="支付宝流水号")

    class Meta:
        db_table="tb_payment"
