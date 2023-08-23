FROM python:3.11-bullseye

WORKDIR /bin
COPY . /bin

RUM mkdir ./data/
RUN apt-get update
RUN apt-get install -y default-mysql-client
RUN pip install --no-cache-dir -r requirements.txt

VOLUME /bin/data
VOLUME /bin/config

ENTRYPOINT ["python3","main.py"]