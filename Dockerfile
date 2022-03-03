FROM alpine:3.11.0a5-alpine3.15

LABEL author "marjamis"

RUN apk add  --no-cache --update python3 apache2 apache2-ssl apache2-mod-wsgi && \
  apk add --no-cache --virtual=build-dependencies wget ca-certificates && \
  wget "https://bootstrap.pypa.io/get-pip.py" -O /dev/stdout | python3 && \
  apk del build-dependencies

RUN pip install virtualenv && \  
  virtualenv --no-site-packages /tmp/main && \  
  source /tmp/main/bin/activate && \  
  pip install django django-bootstrap3 boto


COPY ./configurations/wsgi.conf /etc/apache2/conf.d/
COPY ./app/cloudtrail/ /var/www/localhost/htdocs/cloudtrail/
COPY ./app/informant/ /var/www/localhost/htdocs/informant/
COPY ./app/manage.py /var/www/localhost/htdocs/


RUN source /tmp/main/bin/activate && \
  mkdir /var/www/localhost/htdocs/searches/ && \ 
  chown -R apache:apache /var/www/localhost/htdocs/ && \
  python3 /var/www/localhost/htdocs/manage.py collectstatic --noinput &&\
  python3 /var/www/localhost/htdocs/manage.py migrate --noinput && \
  rm /var/www/localhost/htdocs/manage.py && \
  rm -r /var/www/localhost/htdocs/cloudtrail/static && \
  sed -i 's:lib/apache2/mod_ssl.so:/usr/lib/apache2/mod_ssl.so:g'  /etc/apache2/conf.d/ssl.conf && \
  sed -i 's:lib/apache2/mod_socache_shmcb.so:/usr/lib/apache2/mod_socache_shmcb.so:g' /etc/apache2/conf.d/ssl.conf && \
  mkdir /run/apache2/; chown apache:apache /run/apache2

COPY ./configurations/mod_wsgi.so /usr/lib/apache2/

EXPOSE 80

CMD [ "/usr/sbin/httpd", "-DNO_DETACH", "-DFOREGROUND" ]
