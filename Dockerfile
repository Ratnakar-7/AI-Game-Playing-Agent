FROM python:3.10

ADD src /app

WORKDIR /app

RUN pip install nltk numpy

CMD [ "python", "game.py", "ai", "ai2", "--dim", "4", "--time", "400","--mode", "server" ]
