FROM python:slim
RUN pip install poetry
COPY .env /app/.env
COPY . /app
WORKDIR /app
RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6 wget -y
RUN poetry install
CMD ["poetry", "run", "gunicorn", "-b", "0.0.0.0:3000", "--conf", "gunicorn_conf.py", "webapp:app"]