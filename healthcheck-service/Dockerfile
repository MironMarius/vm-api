FROM node:18 AS builder

WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npx tsc
FROM node:18-slim
WORKDIR /app

COPY --from=builder /app/dist ./dist
COPY --from=builder /app/package*.json ./

RUN npm install --production

ENV API_URL=http://example.com
ENV MACHINE_ID=default-machine-id

CMD ["node", "dist/index.js"]
