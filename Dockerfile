FROM python:2

WORKDIR /usr/src/app

COPY . .

CMD [ "bash", "/usr/src/app/entry.sh" ]