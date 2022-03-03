FROM python:3.11.0a5-alpine3.15

LABEL author "marjamis"

COPY requirements.txt ./

RUN apk add --no-cache --update && \
    pip install --no-cache-dir -r requirements.txt && \
    mkdir -p /var/www/localhost/htdocs/searches


COPY ./configurations/wsgi.conf /etc/apache2/conf.d/
COPY ./app/cloudtrail/ /var/www/localhost/htdocs/cloudtrail/
COPY ./app/informant/ /var/www/localhost/htdocs/informant/
COPY ./app/manage.py /var/www/localhost/htdocs/


WORKDIR /var/www/localhost/htdocs

RUN python manage.py migrate --run-syncdb && \
    python manage.py makemigrations

CMD [ "python", "manage.py", "runserver" ]
