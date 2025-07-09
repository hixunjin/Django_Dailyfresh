# 天天生鲜网站
一个基于 Django 的生鲜电商网站，包含用户管理、商品展示、购物车、订单、支付等功能。

# 技术栈:
✅ 后端框架：
Django 4.2：主框架，处理业务逻辑、路由、视图、模板、ORM 等功能

Celery：处理异步任务（如邮件发送）

Redis：作为 Celery 的消息中间件、Django 缓存后端、验证码存储等

Django-Redis：Redis 缓存支持

Haystack + Whoosh：全文搜索框架

SMTP (QQ邮箱)：邮件服务发送账号激活邮件

✅ 数据库：
MySQL 8+：关系型数据库，用于存储用户、商品、订单等核心数据

✅ 静态资源 / 存储：
MinIO：对象存储服务，用于上传商品图片等文件（兼容 S3 协议）

本地静态资源：通过 STATICFILES_DIRS 管理前端静态文件

✅ 前端：
HTML + CSS + JavaScript

jQuery：实现前端交互（如轮播图、表单验证）

Bootstrap 4：响应式布局与界面美化

TinyMCE：富文本编辑器（商品描述）

✅ 部署环境：
操作系统：Ubuntu

Web服务器：uWSGI

反向代理服务器：Nginx

进程守护：Supervisor



后端
1.登录
![1](https://github.com/user-attachments/assets/fc7ae92b-68a9-443c-a315-629c32bb0db9)

2.注册
![2](https://github.com/user-attachments/assets/f9d526e4-abd6-4030-84a0-c2eb1722ffa8)

3.首页
![3](https://github.com/user-attachments/assets/20824112-05dd-4b8e-980f-4940df50c53c)
![4](https://github.com/user-attachments/assets/bf038a4b-ce09-48d6-8d0a-165940adeb3d)

4.详情页
![5](https://github.com/user-attachments/assets/409a0d88-8fb5-4761-b8f4-0c0cd7589691)



5.购物车
![6](https://github.com/user-attachments/assets/d4c7c694-2abb-46b5-bf85-ec1379fd1e27)


6.订单生产
![7](https://github.com/user-attachments/assets/4fd60421-297c-4580-aa5a-d97c6410a56c)


7.支付
![8](https://github.com/user-attachments/assets/d9e323da-3071-4ea7-a492-42fd0f712a03)
![9](https://github.com/user-attachments/assets/c0a1db1c-bdbd-46a0-a200-692b37e49e06)
![10](https://github.com/user-attachments/assets/c2e0286e-2f20-4232-834f-010bc6ab2fd1)
