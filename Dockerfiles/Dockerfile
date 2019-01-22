FROM python:3.6.6 

RUN groupadd flaskgroup && useradd -m -g flaskgroup -s /bin/bash flask

RUN mkdir -p /app/web
WORKDIR /app/web

COPY requerimientos.txt /app/web
RUN pip install --no-cache-dir -r requerimientos.txt

COPY . /app/web
 
RUN chown -R flask:flaskgroup /app/web
 
USER flask

ENV APP_CONFIG_INV configs.ProductionConfig

#ENTRYPOINT ["/usr/local/bin/gunicorn", "-w 2", "-b", ":8000", "main:app"]

EXPOSE 8000/tcp