FROM python:3.9.6-slim as builder
WORKDIR /home
COPY requirements_ui.txt .
RUN python3 -m venv venv
ENV PATH="/home/venv/bin:$PATH"
RUN python3 -m pip install --upgrade pip -i https://mirrors.ustc.edu.cn/pypi/web/simple && \
    pip3 install -r requirements_ui.txt -i https://mirrors.ustc.edu.cn/pypi/web/simple

FROM python:3.9.6-slim as release
ENV TZ=Asia/Shanghai
ENV PYTHONOPTIMIZE=1
WORKDIR /home
COPY . .
COPY --from=builder /home/venv /home/venv
ADD https://github.com/go-acme/lego/releases/download/v4.14.0/lego_v4.14.0_linux_386.tar.gz  .
RUN tar -xf lego_v4.14.0_linux_386.tar.gz -C /usr/local/bin/ && \
    rm -rf lego_v4.14.0_linux_386.tar.gz 
ENV PATH="/home/venv/bin:$PATH"
EXPOSE 8080
CMD ["sh", "entrypoint.sh"]