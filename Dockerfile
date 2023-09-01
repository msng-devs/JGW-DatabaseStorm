FROM python:3.11-bullseye

WORKDIR /app
COPY . /app

RUN mkdir ./data
RUN apt-get update
RUN apt-get install -y default-mysql-client
RUN pip install --no-cache-dir -r requirements.txt

ENV TZ=Asia/Seoul
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN echo '#!/bin/sh\npython /app/cmd.py "$@"' > /usr/local/bin/databasestorm
RUN chmod +x /usr/local/bin/databasestorm

ENTRYPOINT ["python3","main.py"]