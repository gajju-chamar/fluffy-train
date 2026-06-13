FROM nikolaik/python-nodejs:python3.11-nodejs18

RUN apt-get update -y && apt-get upgrade -y \
    && apt-get install -y --no-install-recommends ffmpeg \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY . /app/
WORKDIR /app/

RUN pip3 install --no-cache-dir --no-deps pytgcalls==2.1.0
RUN pip3 install --no-cache-dir -r requirements.txt

CMD bash start
