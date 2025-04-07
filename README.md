### Overview

This repo includes 3 services, all written in different programming languages:
- `healthcheck-service` is a small Node service written in Typescript, that simulates an app sending heartbeat updates
- `http-api` is a Flask/Python service that can receive and store heartbeats of multiple services and send requests to `vm-service` to create virtual machines
- `vm-service` is written in Go and simulates the creation/deletion of virtual machines


### Setup

Check out this repo and make sure you have Docker installed. You can run all services via the `docker-compose.yaml` file by simply running

```bash
docker compose up
```

If you want an alternate setup, look through READMEs of the various services
and follow the instructions there.

You can also run `http-api` outside of docker for debugging/testing, but you would need to run the postgres container or have a database instance available locally
```bash
docker-compose up -d postgres
```

Check `http-api/README.md` for more information.
