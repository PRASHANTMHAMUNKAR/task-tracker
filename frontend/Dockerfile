#################### stage 1  Build

FROM node:20 AS builder

WORKDIR /app

COPY package*.json ./

RUN npm install

COPY . .

RUN npm test

RUN npm run build

#################### stage 2 Serve

FROM nginx:alpine

WORKDIR /usr/share/nginx/html

COPY nginx.conf /etc/nginx/conf.d/default.conf

COPY --from=builder /app/dist .

EXPOSE 80
