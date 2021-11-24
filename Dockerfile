FROM python:3.8-slim-buster

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt requirements.txt

RUN apt update
RUN apt install ffmpeg -y
RUN pip3 install -r requirements.txt

COPY . .

ENTRYPOINT [ "python", "-u", "bot.py" ]