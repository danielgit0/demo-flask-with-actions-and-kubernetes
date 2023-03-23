FROM python:3.7.3-alpine3.10

COPY ./flaskr /flaskr
COPY ./setup.py /
COPY ./MANIFEST.in /
COPY ./wsgi.py /

RUN pip install --upgrade pip
RUN pip install pyuwsgi==2.0.21
RUN pip install -e .

RUN apk add doas; \
    adduser flask -G wheel; \
    echo 'flask:123' | chpasswd;

USER flask

CMD ["uwsgi", "--http", "0.0.0.0:80", "--master", "-p", "4", "--uid", "flask", "-w", "wsgi:app"]