FROM docker:20.10.24-dind-rootless

RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.tuna.tsinghua.edu.cn/g'  /etc/apk/repositories

RUN apk add python3 py3-pip
RUN  pip config set global.index-url https://pypi.mirrors.ustc.edu.cn/simple/
RUN pip install plumbum jinja2
RUN pip install ifly_ailab
