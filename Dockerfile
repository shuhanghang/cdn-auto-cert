FROM python:3.9.7-slim as builder
ENV PATH="/home/venv/bin:$PATH"
WORKDIR /home
COPY . .
RUN python3 -m venv venv
RUN pip3 install -r requirements.txt -i https://pypi.douban.com/simple

FROM python:3.9.7-slim as release
ENV PATH="/home/venv/bin:$PATH"
ENV TZ=Asia/Shanghai
ENV PYTHONOPTIMIZE=1
WORKDIR /home
COPY --from=builder /home /home
RUN sed -i 's/deb.debian.org/mirrors.ustc.edu.cn/g' /etc/apt/sources.list && \
    apt update && \
    apt install -y socat curl
CMD [ "python3", "cdn_auto_cert_scheduler.py" ]
