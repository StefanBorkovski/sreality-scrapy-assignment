FROM python:3.11

WORKDIR ./scraper

COPY ./aptscraper/requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

ADD ./aptscraper/. /scraper/

EXPOSE 8080

CMD [ "python", "/scraper/run_scraper.py" ]