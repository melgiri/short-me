FROM python:latest

COPY . /root

ENV DOCKER=true

WORKDIR /root

RUN pip3 install --break-system-packages -r requirements.txt

RUN python3 /root/init.py

CMD ["python3", "/root/main.py"]