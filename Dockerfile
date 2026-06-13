FROM nikolaik/python-nodejs:python3.11-nodejs18

RUN apt-get update -y && apt-get install -y ffmpeg \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY . /app/
WORKDIR /app/

RUN python -m pip install \
    --prefer-binary \
    --retries 20 \
    --timeout 120 \
    -r requirements.txt

CMD ["bash", "start"]
