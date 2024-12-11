# 使用华为源 Python 镜像作为基础镜像
FROM swr.cn-north-4.myhuaweicloud.com/ddn-k8s/docker.io/python:3.9-slim-linuxarm64

# 设置工作目录
WORKDIR /app

# 使用国内镜像源更新 apt，并安装依赖
RUN echo "deb https://mirrors.aliyun.com/debian/ stable main contrib non-free" > /etc/apt/sources.list && \
    apt-get update && apt-get install -y \
    wget \
    curl \
    gnupg \
    unzip \
    && rm -rf /var/lib/apt/lists/*

# 使用 wget 下载所需的驱动或文件
RUN wget -O /tmp/GaussDB_driver.zip https://dbs-download.obs.cn-north-1.myhuaweicloud.com/GaussDB/1730887196055/GaussDB_driver.zip

# 解压下载的文件
RUN unzip /tmp/GaussDB_driver.zip -d /tmp/ && rm /tmp/GaussDB_driver.zip

# 复制驱动到临时目录
RUN cp /tmp/GaussDB_driver/Centralized/Hce2_arm_64/GaussDB-Kernel_505.2.0_Hce_64bit_Python.tar.gz /tmp/

# 解压版本对应驱动包
RUN tar -zxvf /tmp/GaussDB-Kernel_505.2.0_Hce_64bit_Python.tar.gz -C /tmp/ && rm /tmp/GaussDB-Kernel_505.2.0_Hce_64bit_Python.tar.gz

# 将 psycopg2 复制到 python 安装目录下的 site-packages 文件夹下
RUN cp /tmp/psycopg2 $(python3 -c 'import site; print(site.getsitepackages()[0])') -r

# 修改 psycopg2 目录权限为 755
RUN chmod 755 $(python3 -c 'import site; print(site.getsitepackages()[0])')/psycopg2 -R

# 将 psycopg2 目录添加到环境变量 $PYTHONPATH，并使之生效
# 使用 ENV 而不是 export，因为 RUN 会在每一步创建新的 shell
ENV PYTHONPATH="${PYTHONPATH}:$(python3 -c 'import site; print(site.getsitepackages()[0])')"

# 对于非数据库用户，需要将解压后的 lib 目录，配置在 LD_LIBRARY_PATH 中
# 同样使用 ENV 设置环境变量
ENV LD_LIBRARY_PATH="/tmp/lib:$LD_LIBRARY_PATH"

# 将 requirements.txt 文件复制到容器中
COPY requirements.txt /app/

# 安装依赖
RUN pip install --no-cache-dir -r requirements.txt

# 安装 Gunicorn
RUN pip install gunicorn

# 将项目代码复制到容器中
COPY . /app/

# 暴露应用运行的端口
EXPOSE 8000

# 启动服务，绑定到 0.0.0.0:8000
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "user-service.wsgi:application"]
