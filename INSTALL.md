Stucampus installation
=====

1. 安装[python](https://www.python.org/downloads/)
2. 安装[easy_install](https://pypi.python.org/pypi/setuptools#installation-instructions)
3. 安装[pip](https://pip.pypa.io/en/stable/installing.html)
4. 复制一份 `stucampus/config/production.py.sample` 重命名为`stucampus/config/prodcution.py`
5. 根据自己系统的情况修改`stucampus/config/production.py`文件里的内容。
6. 用`pip install -r requirements.txt`命令安装所需依赖包
7. 用`sudo apt-get install libxml2-dev libxslt1-dev`命令安装xml2库和xslt库
8. 用`sudo apt-get install PIL --allow-external PIL --allow-unverified PIL`命令安装[PIL](https://pypi.python.org/pypi/Pillow/2.2.1)
9. 用`python manage.py syncdb`命令创建项目所需数据库。([syncdb](https://docs.djangoproject.com/en/1.5/ref/django-admin/#syncdb))
10. 用`python manage.py runserver`命令运行项目([runserver](https://docs.djangoproject.com/en/1.5/ref/django-admin/#runserver-port-or-address-port))

###### 注意事项

* 在本地调试时，数据库可用sqlite
* 项目所使用的Django版本为1.5.1, 查阅[文档](https://docs.djangoproject.com/en/1.5/)时请留意版本。
* 以上命令中`apt-get`为ubuntu的包管理器。若使用其他非Debian系系统，请根据自行需要使用相应命令(centos 通常为yum, 则命令应该为yum install ****, 包名也可能会有所差异，请自行解决)。
* 第4步可在第9步之前的任意时候操作
