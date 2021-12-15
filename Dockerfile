FROM python:3.8-slim-buster

EXPOSE 6969

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt update
RUN apt install ffmpeg -y

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

ENTRYPOINT [ "python", "-u", "bot.py" ]