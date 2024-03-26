FROM python:3.11

WORKDIR ./app

COPY ./flask_app/requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

ADD ./flask_app/. /app/

CMD ["python", "/app/app.py"]