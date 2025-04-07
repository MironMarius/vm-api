### Healthcheck service

This is small service used to send healthchecks from virtual machines to an
external endpoint.

#### Running with Docker

```bash
docker build -t healthcheck-service .
docker run -p 8888:8888 -e API_URL=https://api.example.com -e MACHINE_ID=your-machine-id healthcheck-service
```

### Running without Docker

Copy `.env.sample` to `.env` and modify to your liking.

Install dependencies with `npm install` and build the service with `npx tsc`.

Finally, run the application with `node dist/index.js`

