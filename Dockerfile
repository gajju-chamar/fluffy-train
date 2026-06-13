RUN pip install --upgrade pip setuptools wheel

RUN pip install \
    --prefer-binary \
    --retries 20 \
    --timeout 120 \
    -r requirements.txt
