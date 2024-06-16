FROM python:3.11-slim

# Для отправки пакетов
RUN pip install scapy

# Для пинга
RUN apt-get update && apt-get install -y iputils-ping

COPY find_mtu.py /app/

WORKDIR /app

ENTRYPOINT ["python", "find_mtu.py"]
