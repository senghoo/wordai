FROM python:3.7

RUN curl -sL https://deb.nodesource.com/setup_12.x | bash -

RUN apt-get update && apt-get install -y\
  build-essential libpq-dev nodejs nginx-extras

ENV NODE_PATH /usr/lib/node_modules

RUN pip install uwsgi

WORKDIR /usr/src/app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY ui/package.json ./ui/

WORKDIR /usr/src/app/ui
RUN npm install


COPY . /usr/src/app

ENV NODE_ENV production
RUN npm run build
WORKDIR /usr/src/app
COPY nginx.conf /etc/nginx/
COPY nginx-server.conf /etc/nginx/sites-enabled/default
EXPOSE 80
CMD './start.sh'
