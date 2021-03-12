FROM node:12-alpine

COPY . /src
WORKDIR /src

COPY package*.json ./

RUN yarn install

EXPOSE 8080

CMD ["yarn", "serve"]
