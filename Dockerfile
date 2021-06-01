FROM python:3.8.0-slim

WORKDIR /app
COPY . /app 

RUN apt-get update \
&& apt-get install gcc -y \
&& apt-get clean

RUN pip3 install -r requirements.txt

CMD ["python3", "Miku.py"]
