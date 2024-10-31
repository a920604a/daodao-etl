# 使用官方 Airflow 映像作為基礎
FROM apache/airflow:2.10.0-python3.10

USER root
RUN apt-get update && apt-get install -y \
    && rm -rf /var/lib/apt/lists/*

RUN apt-get update && apt-get install -y \
    libpq-dev gcc 

# 切換回 Airflow 使用者
USER airflow
COPY requirements.txt /requirements.txt
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r /requirements.txt

