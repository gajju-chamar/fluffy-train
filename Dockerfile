FROM nikolaik/python-nodejs:python3.11-nodejs18

RUN apt-get update -y && apt-get install -y ffmpeg \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY . /app/
WORKDIR /app/

RUN pip install --upgrade pip
RUN pip install --retries 5 -r requirements.txt

CMD bash start
