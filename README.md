# DWS+Django Demo

此Demo主要使用Django+DWS提供RESTful API功能。
此项目依赖条件如下：

1. 拥有DWS集群8.0.0及以上版本
2. 通过这两个项目初始化数据：[jaffle-shop-gaussdb](https://github.com/pangpang20/jaffle-shop-gaussdb)和[jaffle-shop-dws](https://github.com/pangpang20/jaffle-shop-dws),前一个项目为DWS初始化数据，后一个项目为在DWS加工数据，本项目把最终的结果数据通过Django提供RESTful API给用户使用。

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

# 安装依赖

```bash
pip install --no-cache-dir -r requirements.txt
pip install gunicorn

```

# 安装华为GaussDB Python驱动

由于开源的psycopg2驱动，不兼容DWS默认密码加密方式，需要使用华为的GaussDB Python驱动。

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
export PYTHONPATH="${PYTHONPATH}:$(python3 -c 'import site; print(site.getsitepackages()[0])')"

# 对于非数据库用户，需要将解压后的 lib 目录，配置在 LD_LIBRARY_PATH 中
export LD_LIBRARY_PATH="/tmp/lib:$LD_LIBRARY_PATH"

# 测试是否可以使用 psycopg2,没有报错即可
python3
Python 3.9.9 (main, Jun 19 2024, 02:50:21)
[GCC 10.3.1] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> import psycopg2
>>> exit()
```

# 修改配置文件

复制配置文件`user-service/sample-settings.py`为`user-service/settings.py`将DWS的连接信息your_开头的修改为实际值。

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'your_database',
        'USER': 'your_username',
        'PASSWORD': 'your_password',
        'HOST': 'your_host',
        'PORT': your_port,
        'OPTIONS': {
            'options': '-c search_path=your_schema,public'
        },
    }
}
```

# 启动服务

```bash
cd resource-service-python
# 创建迁移
python manage.py makemigrations django_dws

# 执行迁移
python manage.py migrate django_dws

# 启动服务，默认端口为8000
python manage.py runserver 0.0.0.0:8000

# 也可以使用gunicorn启动服务
gunicorn --bind 0.0.0.0:8000  user-service.wsgi:application

```
