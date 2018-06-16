DOCKER_BASE_IMAGE_TAG := beasley_weather_base
DOCKER_SERVER_IMAGE_TAG := server_weewx
DOCKER_CLIENT_IMAGE_TAG := client_weewx
DOCKER_TRANSFER_CLIENT_TAG := client_transfer_client

up.server:
	docker-compose -f docker/server/docker-compose.yml -p server up

up.dev.server:
	docker-compose -f docker/server/docker-compose.yml \
	               -f docker/server/docker-compose.dev.yml \
	               -p server up

up.station:
	docker-compose -f docker/station/docker-compose.yml -p station up

up.dev.station:
	docker-compose -f docker/station/docker-compose.yml \
	               -f docker/station/docker-compose.dev.yml \
	               -p station up

docker.build.base:
	docker build -f docker/base/Dockerfile -t $(DOCKER_BASE_IMAGE_TAG) .

docker.build.transfer-client:
	docker build -f docker/transfer-client/Dockerfile -t $(DOCKER_TRANSFER_CLIENT_TAG) .

docker.build.server:
	docker build -f docker/server/Dockerfile -t $(DOCKER_SERVER_IMAGE_TAG) .

docker.build.station:
	docker build -f docker/station/Dockerfile -t $(DOCKER_CLIENT_IMAGE_TAG) .
