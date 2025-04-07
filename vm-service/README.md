### VM service

This small service is used to create and delete virtual machines.

#### Running with Docker

```bash
docker build -t go-vm-app .
docker run -p 8080:8080 go-vm-app
```
#### Running without Docker

Fetch dependencies
```
go mod tidy
```

Build the application

```
go build
```

Run the application

```
./vm-service

```

#### API docs

The service exposes two endpoints, `/create` and `/delete` respectively.

##### Create can be called with these parameters

```bash
curl -X POST -H "Content-Type: application/json" \
-d '{"image":"ubuntu:20.04","name":"my-vm","ports":[[22,22],[80,8080]],"resources":{"cpu":2,"memory":2048}}' \
http://localhost:8080/create
```

##### Delete can be called with these parameters

```bash
curl -X DELETE -H "Content-Type: application/json" -d '{"uuid": "your-uuid-here"}' \
http://localhost:8080/delete

```
