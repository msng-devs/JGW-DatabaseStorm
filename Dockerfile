FROM 3.11-bullseye

WORKDIR /bin
COPY . /bin

RUN apt-get update
RUN apt-get install default-mysql-client
RUN pip install --no-cache-dir -r requirements.txt

VOLUME /bin/data
VOLUME /bin/config

CMD python3 main.py