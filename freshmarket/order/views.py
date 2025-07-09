from datetime import datetime

from django.shortcuts import render,redirect
from django.views import View
from django_redis import get_redis_connection
from goods.models import *
from user.models import *
from django.db import transaction
from django.http import JsonResponse
from order.models import *
from django.conf import settings
import os
from alipay import AliPay
from django.urls import reverse
from utils.mixin import LoginRequiredMixin


class OrderPlaceView(View):
    """提交订单页面的显示"""
    def post(self,request):
        sku_ids =  request.POST.getlist('sku_ids')
        user = request.user

        #参数校验
        if not sku_ids:
            return redirect(reversed('cart:show'))

        #创建 Redis 连接对象
        conn = get_redis_connection('default')
        cart_key = 'cart_%d' % user.id

        #创建变量保存商品的总数量和总价格
        total_count = 0
        total_price = 0
        skus = []
        #遍历id列表，进行数据处理
        for sku_id in sku_ids:
            sku = GoodsSKU.objects.get(id=sku_id)

            #获取商品数量
            count = conn.hget(cart_key,sku_id)
            #商品小计
            amount = sku.price * int(count)

            #动态给模型实例赋值，商品数量和商品小计
            sku.count = int(count)
            sku.amount = amount

            #添加到列表中
            skus.append(sku)

            #商品总数量和总价累加
            total_count += int(count)
            total_price += amount


        #运费
        transit_price = 10

        #实际付款
        total_pay = transit_price + total_price

        #获取用户的地址
        addrs = Address.objects.filter(user=user)  #直接这样就可以查询出对应的用户

        #组织上下文
        sku_ids =','.join(sku_ids)

        context = {'skus': skus,
                   'total_count': total_count,
                   'total_price': total_price,
                   'transit_price': transit_price,
                   'total_pay': total_pay,
                   'addrs': addrs,
                   'sku_ids': sku_ids
                   }

        return render(request,'place_order.html',context)






#创建订单业务逻辑
#整体逻辑就是，用户每购买一个商品，就加入到订单信息表，同时将商品数量添加到订单表中

class OrderCommitView1(View):
    """订单创建"""

    # 事务装饰器
    @transaction.atomic
    def post(self, request):
        """订单创建"""
        # 判断用户是否登录,非后台无法使用LoginRequiredMixin验证
        user = request.user
        if not user.is_authenticated:
            # 用户美登录
            return JsonResponse({'res': 0, 'errmsg': '用户为登录'})

        # 接受参数
        addr_id = request.POST.get('addr_id')
        pay_method = request.POST.get('pay_method')
        sku_ids = request.POST.get('sku_ids')

        # 校验参数
        if not all([addr_id, pay_method, sku_ids]):
            return JsonResponse({'res': 1, 'errmsg': '参数不完整'})

        # 校验支付方式
        if pay_method not in OrderInfo.PAY_METHODS.keys():
            return JsonResponse({'res': 2, 'errmsg': '非法的支付方式'})

        # 校验地址
        try:
            addr = Address.objects.get(id=addr_id)
        except Address.DoesNotExist:
            # 地址不存在
            return JsonResponse({'res': 3, 'errmsg': '地址不存在'})

        # todo: 创建订单核心业务

        # 组织参数
        # 订单id： 年月日时间+用户id
        order_id = datetime.now().strftime('%Y%m%d%H%M%S') + str(user.id)

        # 运费
        transit_price = 10

        # 总数目和总金额
        total_count = 0
        total_price = 0

        # 设置事务保存点
        save_id = transaction.savepoint()
        try:
            # todo： 向df_order_info表中添加一条记录
            order = OrderInfo.objects.create(order_id=order_id,
                                             user=user,
                                             addr=addr,
                                             pay_method=pay_method,
                                             total_count=total_count,
                                             total_price=total_price,
                                             transit_price=transit_price)

            # todo： 用户的订单中有几个商品，需要向df_order_goods表中加入几条记录
            conn = get_redis_connection('default')
            cart_key = 'cart_%d' % user.id

            sku_ids = sku_ids.split(',')
            for sku_id in sku_ids:
                for i in range(3):
                    # 获取商品的信息
                    try:
                        sku = GoodsSKU.objects.get(id=sku_id)
                    except:
                        # 商品不存在
                        transaction.savepoint_rollback(save_id)
                        return JsonResponse({'res': 4, 'errmsg': '商品不存在'})

                    # 从redis中获取用户所要购买的商品的数量
                    count = conn.hget(cart_key, sku_id)

                    # todo：判断商品的库存
                    if int(count) > sku.stock:
                        transaction.savepoint_rollback(save_id)
                        return JsonResponse({'res': 6, 'errmsg': ' 商品库存不足'})

                    # todo: 更新商品的库存和销量
                    orgin_stock = sku.stock
                    new_stock = orgin_stock - int(count)
                    new_sales = sku.sales + int(count)

                    # update df_goods_sku set stock=new_stock, sales=new_sales
                    # where id=sku_id and stock = orgin_stock
                    # 返回受影响的行数
                    res = GoodsSKU.objects.filter(id=sku_id, stock=orgin_stock).update(stock=new_stock, sales=new_sales)
                    if res == 0:
                        if i == 2:
                            # 尝试第三次
                            transaction.savepoint_rollback(save_id)
                            return JsonResponse({'res': 7, 'errmsg': '下单失败2'})
                        continue

                    # todo：向df_order_goods表中添加一条记录
                    OrderGoods.objects.create(order=order,
                                              sku=sku,
                                              count=count,
                                              price=sku.price)



                    # todo: 累加计算订单商品的总数量和总价格
                    amount = sku.price * int(count)
                    total_count += int(count)
                    total_price += amount

                    # 跳出循环
                    break

            # todo: 更新订单信息表中的商品的总数量和总价格
            order.total_count = total_count
            order.total_price = total_price
            order.save()
        except Exception as e:
            transaction.savepoint_rollback(save_id)
            return JsonResponse({'res': 7, 'errmsg': '下单失败'})

        # 提交事务
        transaction.savepoint_commit(save_id)

        # todo： 清楚用户购物车中对应的记录 [1, 3]
        conn.hdel(cart_key, *sku_ids)  # 拆包

        # 返回应答
        return JsonResponse({'res': 5, 'message': '创建成功'})





#订单支付，配合前端的 POST 请求，完成这个功能
class OrderPayView(View):
    """订单支付"""
    def post(self,request):
        user = request.user
        if not user.is_authenticated:
            return  JsonResponse({'res':0,'errmsg':'请先进行登录!'})

        #接收参数
        order_id = request.POST.get('order_id')

        #校验参数
        if not order_id:
            return JsonResponse({'res':1,'errmsg':'订单编号不存在'})

        #查询数据库中的订单编号，并验证是否有效
        try:
            order = OrderInfo.objects.get(
                order_id=order_id,
                user=user,
                pay_method=3,
                order_status=1
            )
        except OrderInfo.DoesNotExist:
            return JsonResponse({'res':2,'errmsg':'无效订单'})

        #配置两个密钥文件地址
        app_private_key_string =open(os.path.join(settings.BASE_DIR,'order/app_private_key.pem')).read()
        alipay_public_key_string = open(os.path.join(settings.BASE_DIR, 'order/alipay_public_key.pem')).read()

        # 业务处理：使用Python sdk调用支付宝的支付接口
        # 初始化

        alipay = AliPay(
            appid = '9021000149692412',
            app_notify_url=None,  # 默认回调url
            app_private_key_string=app_private_key_string,
            # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
            alipay_public_key_string=alipay_public_key_string,
            sign_type="RSA2",  # RSA 或者 RSA2
            debug=True  # 默认False True就会访问沙箱地址
        )

        # 调用支付接口
        # 电脑网站支付，需要跳转到https://openapi.alipaydev.com/gateway.do? + order_string
        total_pay = order.total_price + order.transit_price  # Decimal格式
        order_string = alipay.api_alipay_trade_page_pay(
            out_trade_no=order_id,  # 订单id
            total_amount=str(total_pay),
            subject='阿伟电商网站%s' % order_id,
            return_url=None,
            notify_url=None  # 可选, 不填则使用默认notify url
        )

        # 返回应答
        #下面的地址
        pay_url = 'https://openapi-sandbox.dl.alipaydev.com/gateway.do?' + order_string
        return JsonResponse({'res': 3, 'pay_url': pay_url})





#接下来剩余两个功能
#检查支付功能
#下面的功能也是通过 Ajax 发起 POST 请求，这种请求有种标志，那就是它返回的数据是 JSON 数据

class CheckPayView(View):
    def post(self, request):
        user = request.user
        if not user.is_authenticated:
            return JsonResponse({'res': 0, 'errmsg': '请先进行登录!'})

        # 接收参数
        order_id = request.POST.get('order_id')

        # 校验参数
        if not order_id:
            return JsonResponse({'res': 1, 'errmsg': '订单编号不存在'})

        # 查询数据库中的订单编号，并验证是否有效
        try:
            order = OrderInfo.objects.get(
                order_id=order_id,
                user=user,
                pay_method=3,
                order_status=1
            )
        except OrderInfo.DoesNotExist:
            return JsonResponse({'res': 2, 'errmsg': '无效订单'})

        # 配置两个密钥文件地址
        app_private_key_string = open(os.path.join(settings.BASE_DIR, 'order/app_private_key.pem')).read()
        alipay_public_key_string = open(os.path.join(settings.BASE_DIR, 'order/alipay_public_key.pem')).read()

        # 业务处理：使用Python sdk调用支付宝的支付接口
        # 初始化

        alipay = AliPay(
            appid='9021000149692412',
            app_notify_url=None,  # 默认回调url
            app_private_key_string=app_private_key_string,
            # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
            alipay_public_key_string=alipay_public_key_string,
            sign_type="RSA2",  # RSA 或者 RSA2
            debug=True  # 默认False True就会访问沙箱地址
        )

        #调用支付宝查询接口
        #循环的一种用法，有时候我们不知道一个功能是否需要循环，可以先编写这个功能，当发现一段代码需要多次
        #执行才能得到预期的结果，这个时候直接把代码放到循环中即可
        while True:
            response = alipay.api_alipay_trade_query(order_id)
            code  = response.get('code')
            if code == '10000' and response.get('trade_status') =='TRADE_SUCCESS':
                #支付成功
                #获取支付宝交易号
                trade_no = response.get('trade_no')

                #更新订单状态（注意，我们没有发货和收获这个环节，直接就是支付和评价）
                #下面是通过更新数据表字段
                order.trade_no = trade_no
                order.order_status = 4 #待评价状态
                order.save()

                #返回结果
                return  JsonResponse({'res':3,'message':'支付成功'})
            elif code =='40004'or(code == '10000' and response.get('trade_status') == 'WAIT_BUYER_PAY'):
                import time
                time.sleep(5)
                continue
            else:
                return  JsonResponse({'res':4,'errmsg':'支付失败'})



class CommentView(LoginRequiredMixin, View):
    """订单评论"""
    def get(self, request, order_id):
        """提供评论页面"""
        user = request.user
        # 校验数据
        if not order_id:
            return redirect(reverse('user:order'))

        try:
            order = OrderInfo.objects.get(order_id=order_id, user=user)
        except OrderInfo.DoesNotExist:
            return redirect(reverse("user:order"))

        # 根据订单的状态获取订单的状态标题
        order.status_name = OrderInfo.ORDER_STATUS[order.order_status]

        # 获取订单商品信息
        order_skus = OrderGoods.objects.filter(order_id=order_id)
        for order_sku in order_skus:
            # 计算商品的小计
            amount = order_sku.count*order_sku.price
            # 动态给order_sku增加属性amount,保存商品小计
            order_sku.amount = amount
        # 动态给order增加属性order_skus, 保存订单商品信息
        order.order_skus = order_skus

        # 使用模板
        return render(request, "order_comment.html", {"order": order})

    def post(self, request, order_id):
        """处理评论内容"""
        user = request.user
        # 校验数据
        if not order_id:
            return redirect(reverse('user:order'))

        try:
            order = OrderInfo.objects.get(order_id=order_id, user=user)
        except OrderInfo.DoesNotExist:
            return redirect(reverse("user:order"))

        # 获取评论条数
        total_count = request.POST.get("total_count")
        total_count = int(total_count)

        # 循环获取订单中商品的评论内容
        for i in range(1, total_count + 1):
            # 获取评论的商品的id
            sku_id = request.POST.get("sku_%d" % i) # sku_1 sku_2
            # 获取评论的商品的内容
            content = request.POST.get('content_%d' % i, '') # cotent_1 content_2 content_3
            try:
                order_goods = OrderGoods.objects.get(order=order, sku_id=sku_id)
            except OrderGoods.DoesNotExist:
                continue

            order_goods.comment = content
            order_goods.save()

        order.order_status = 5 # 已完成
        order.save()

        return redirect(reverse("user:order", kwargs={"page": 1}))























































































































