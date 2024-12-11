# DWS+Django Demouom
此Demo主要使用Django+DWS提供RESTful API功能，方便对项目进行体验或验收使用。

目录结构说明：
```python

resource-service-python/
├── django_dws
│   ├── admin.py
│   ├── apps.py
│   ├── __init__.py
│   ├── models.py  # 模型类文件
│   ├── tests.py
│   ├── urls.py # 路由文件
│   └── views.py # 视图文件
├── Dockerfile
├── manage.py
├── README.md
├── requirements.txt
├── templates
│   └── home.html
└── user-service
    ├── asgi.py
    ├── __init__.py
    ├── settings.py # 配置文件
    ├── urls.py  # 主路由文件
    └── wsgi.py
```


# 安装华为GaussDB Python驱动
由于开源的psycopg2驱动，不兼容密码加密方式为2，需要使用华为的GaussDB Python驱动。
```bash
# 华为云官网获取驱动包
wget -O /tmp/GaussDB_driver.zip https://dbs-download.obs.cn-north-1.myhuaweicloud.com/GaussDB/1730887196055/GaussDB_driver.zip

# 解压下载的文件
unzip /tmp/GaussDB_driver.zip -d /tmp/ && rm -rf /tmp/GaussDB_driver.zip

# 复制驱动到临时目录
\cp /tmp/GaussDB_driver/Centralized/Hce2_arm_64/GaussDB-Kernel_505.2.0_Hce_64bit_Python.tar.gz /tmp/

# 解压版本对应驱动包
tar -zxvf /tmp/GaussDB-Kernel_505.2.0_Hce_64bit_Python.tar.gz -C /tmp/ && rm -rf /tmp/GaussDB-Kernel_505.2.0_Hce_64bit_Python.tar.gz

# 卸载原生psycopg2
pip uninstall -y $(pip list | grep psycopg2 | awk '{print $1}')


# 将 psycopg2 复制到 python 安装目录下的 site-packages 文件夹下
\cp /tmp/psycopg2 $(python3 -c 'import site; print(site.getsitepackages()[0])') -r

# 修改 psycopg2 目录权限为 755
chmod 755 $(python3 -c 'import site; print(site.getsitepackages()[0])')/psycopg2 -R

# 将 psycopg2 目录添加到环境变量 $PYTHONPATH，并使之生效
echo 'export PYTHONPATH="${PYTHONPATH}:$(python3 -c '\''import site; print(site.getsitepackages()[0])'\'')"' >> .venv/bin/activate

# 对于非数据库用户，需要将解压后的 lib 目录，配置在 LD_LIBRARY_PATH 中
echo 'export LD_LIBRARY_PATH="/tmp/lib:$LD_LIBRARY_PATH"' >> .venv/bin/activate

# 测试是否可以使用 psycopg2,没有报错即可
python3
Python 3.9.9 (main, Jun 19 2024, 02:50:21)
[GCC 10.3.1] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> import psycopg2
>>> exit()
```

在项目根目录下执行以下命令安装插件
```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install --upgrade pip
pip install django

```



# 启动服务

```bash

# 创建迁移
python manage.py makemigrations django_dws

# 执行迁移
python manage.py migrate django_dws

# 启动服务，端口为8000
python manage.py runserver 0.0.0.0:8000

# 也可以使用uwsgi启动服务
uwsgi --http 0.0.0.0:8000 --module user-service.wsgi
```
