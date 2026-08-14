# frontend/Dockerfile
#
# Multi-stage build: compile the React app with Node, then serve the
# resulting static files with a lightweight nginx image (much smaller
# and faster than shipping Node itself into the final image).

# --- Stage 1: build ---
FROM node:20-alpine AS build

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .

# VITE_API_URL must be provided at BUILD time (Vite bakes client-side env
# vars into the static bundle when `npm run build` runs -- there is no
# "runtime" env var step for a static site). Passed in via docker-compose
# or `docker build --build-arg VITE_API_URL=...`.
ARG VITE_API_URL
ENV VITE_API_URL=$VITE_API_URL

RUN npm run build

# --- Stage 2: serve ---
FROM nginx:alpine

COPY --from=build /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
