DOCKER_BASE_IMAGE_TAG := beasleyweatherstation/base
DOCKER_SERVER_IMAGE_TAG := beasleyweatherstation/server
DOCKER_CLIENT_IMAGE_TAG := beasleyweatherstation/station
DOCKER_TRANSFER_CLIENT_TAG := beasleyweatherstation/transfer-client

down.server:
	cd docker/server && docker-compose down

up.server:
	docker-compose -f docker/server/docker-compose.yml -p server up

up.serverd:
	docker-compose -f docker/server/docker-compose.yml -p server up -d

up.dev.server:
	docker-compose -f docker/server/docker-compose.yml \
	               -f docker/server/docker-compose.dev.yml \
	               -p server up

up.dev.serverd:
	docker-compose -f docker/server/docker-compose.yml \
	               -f docker/server/docker-compose.dev.yml \
	               -p server up \
				   -d

down.station:
	cd docker/station && docker-compose down

up.station:
	docker-compose -f docker/station/docker-compose.yml -p station up

up.stationd:
	docker-compose -f docker/station/docker-compose.yml -p station up -d

up.dev.station:
	docker-compose -f docker/station/docker-compose.yml \
	               -f docker/station/docker-compose.dev.yml \
	               -p station up

up.dev.stationd:
	docker-compose -f docker/station/docker-compose.yml \
	               -f docker/station/docker-compose.dev.yml \
	               -p station up \
				   -d

docker.build.base:
	docker build -f docker/base/Dockerfile -t $(DOCKER_BASE_IMAGE_TAG) .

docker.build.transfer-client:
	docker build -f docker/transfer-client/Dockerfile -t $(DOCKER_TRANSFER_CLIENT_TAG) .

docker.build.server:
	docker build -f docker/server/Dockerfile -t $(DOCKER_SERVER_IMAGE_TAG) .

docker.build.station:
	docker build -f docker/station/Dockerfile -t $(DOCKER_CLIENT_IMAGE_TAG) .
