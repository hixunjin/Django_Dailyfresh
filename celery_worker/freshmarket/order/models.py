from django.db import models
from db.base_model import BaseModel
# Create your models here.



class OrderInfo(BaseModel):
    """支付方式"""
    PAY_METHOD_CHOICES = (
        (1, "货到付款"),
        (2,"微信支付"),
        (3, "支付宝"),
        (4, '银联支付')
    )


    #订单状态

    ORDER_STATUS_CHOICES = (
        (1, '待支付'),
        (2, '待发货'),
        (3, '待收货'),
        (4, '待评价'),
        (5, '已完成')
    )


    #模型字段
    order_id = models.CharField(max_length=128,primary_key=True,verbose_name="订单id")
    user =models.ForeignKey('user.User',on_delete=models.CASCADE,verbose_name="用户")
    addr = models.ForeignKey('user.Address',on_delete=models.CASCADE,verbose_name="地址")

    #支付方式，默认是支付宝
    pay_ment = models.SmallIntegerField(choices=PAY_METHOD_CHOICES,default=3,verbose_name="支付方式")

    #商品数量、商品单价、订单运费
    total_count = models.IntegerField(default=1,verbose_name="商品数量")
    total_price = models.DecimalField(max_digits=10,decimal_places=2,verbose_name="商品总价")
    transit_price = models.DecimalField(max_digits=10,decimal_places=2,verbose_name="订单运费")

    #这样选择性的数据，本质存储的是数字，因此选择一个数字类型，然后在参数 choices 等于提前编写好的元组，再指定默认数据（以数字表示）
    order_status = models.SmallIntegerField(choices=ORDER_STATUS_CHOICES,default=1,verbose_name="订单状态")
    trade_no = models.CharField(max_length=128, verbose_name='支付编号')

    class Meta:
        db_table = 'df_order_info'
        verbose_name = '订单'
        verbose_name_plural = verbose_name




#订单商品模型
class OrderGoods(BaseModel):

    #订单、商品SKU、商品数量、商品价格、评论
    order =models.ForeignKey('OrderInfo',on_delete=models.CASCADE,verbose_name="订单")
    sku = models.ForeignKey('goods.GoodsSKU',on_delete=models.CASCADE,verbose_name="商品SKU")
    count = models.IntegerField(default=1,verbose_name="商品数目")
    price = models.DecimalField(max_digits=10,decimal_places=2,verbose_name="商品价格")
    comment = models.CharField(max_length=256,default='',verbose_name="评论")


    class Meta:
        db_table = 'df_order_goods'
        verbose_name = '订单商品'
        verbose_name_plural = verbose_name






















