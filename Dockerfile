FROM --platform=linux/arm64 ubuntu:22.04

WORKDIR /app


ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y \
    ca-certificates \
    wget \
    curl \
    gnupg \
    unzip \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

RUN echo "deb [arch=arm64] https://mirrors.tuna.tsinghua.edu.cn/ubuntu-ports/ jammy main restricted universe multiverse" > /etc/apt/sources.list && \
    echo "deb [arch=arm64] https://mirrors.tuna.tsinghua.edu.cn/ubuntu-ports/ jammy-updates main restricted universe multiverse" >> /etc/apt/sources.list && \
    echo "deb [arch=arm64] https://mirrors.tuna.tsinghua.edu.cn/ubuntu-ports/ jammy-security main restricted universe multiverse" >> /etc/apt/sources.list


RUN apt-get update && apt-get install -y \
    wget \
    curl \
    gnupg \
    unzip \
    python3 \
    python3-pip \
    python3-distutils \
    python3-venv \
    gettext \
    net-tools \
    iputils-ping \
    gnutls-bin \
    libgnutls30 \
    vim \
    && rm -rf /var/lib/apt/lists/*

ARG DB_NAME
ARG DB_USER
ARG DB_PASSWORD
ARG DB_HOST
ARG DB_PORT



COPY . /app/
RUN pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple && \
    python3 -m pip install --upgrade pip


RUN pip install --no-cache-dir -r requirements.txt && \
    pip install gunicorn

RUN wget -O /tmp/GaussDB_driver.zip https://dbs-download.obs.cn-north-1.myhuaweicloud.com/GaussDB/1730887196055/GaussDB_driver.zip && \
    unzip /tmp/GaussDB_driver.zip -d /tmp/ && \
    rm -rf /tmp/GaussDB_driver.zip && \
    \cp /tmp/GaussDB_driver/Centralized/Hce2_arm_64/GaussDB-Kernel_505.2.0_Hce_64bit_Python.tar.gz /tmp/ && \
    tar -zxvf /tmp/GaussDB-Kernel_505.2.0_Hce_64bit_Python.tar.gz -C /tmp/ && \
    rm -rf /tmp/GaussDB-Kernel_505.2.0_Hce_64bit_Python.tar.gz && \
    rm -rf /tmp/GaussDB_driver && \
    \cp /tmp/psycopg2 $(python3 -c 'import site; print(site.getsitepackages()[0])') -r && \
    chmod 755 $(python3 -c 'import site; print(site.getsitepackages()[0])')/psycopg2 -R

ENV PYTHONPATH="${PYTHONPATH}:$(python3 -c 'import site; print(site.getsitepackages()[0])')"
ENV LD_LIBRARY_PATH="/tmp/lib:$LD_LIBRARY_PATH"
RUN mv /app/user-service/sample-settings.py /app/user-service/settings.py

EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "user-service.wsgi:application"]
