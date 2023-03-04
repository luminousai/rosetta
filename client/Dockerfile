FROM node:19

WORKDIR /app

COPY src src
COPY package.json .
COPY package-lock.json .
COPY webpack.config.js .
COPY .babelrc .

RUN npm ci

EXPOSE 8080

