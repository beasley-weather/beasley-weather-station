# Beasley Weather Station

The system currently consists of a Weather Station Client and a Server. The Weather
Station Client has a Acurite weather station connected via usb, runs Weewx and a Transfer
System to transfer data to the Server. The Server runs a Transfer System Server to accept
data from the weather station and generates Weewx reports which are served via Nginx.

All the components required to run the whole system are containerized using Docker and
composed using Docker Compose. It is possible to run the individuals components on the
weather station client and server on the host OS, but you will need to install
dependencies manually. The containers are self contained and provide everything needed to
run the software.

Linux is assumed to be the host OS. Windows compatibility with the weather station client
Weewx unknown. If it is possible to pass through a USB device to a container, then it
should be possible to run the weather station client on a Windows host. The Server should
run on a Windows host without issue.

## Getting the Container Images

The Docker Hub Organization for this project is
https://hub.docker.com/u/beasleyweatherstation/dashboard/

You may wish to check there if pre-built images for the platform architecture you're
targgetting are available (x86, x86-64, arm, etc). The `docker-compose.yml` files for the
station and server (found in the respective `station/` and `server/` directories in side
the `docker/` directory) may need to be updated with a particular image value if you're
targeting a specific build version or architecture.

```
services:
  ...
    image: beasleyweatherstation/station
```

The `image` value is of the form `namespace/image_name:tag`, where the `:tag` is
optional. In the above example, the namespace is 'beasleyweatherstation', image name is
'station' and there is no tag.

If you're unable to find a usable pre-built image, you can build one locally. In order to
specify a image name(s), you need to update the `DOCKER_X_IMAGE_TAG` variable(s) in the
`Makefile` at the root of this repository. For example, you can built a set of images
that target the 'arm v7' architecture and assign them a `armv7-N` tag, where N is some
version number.

```
DOCKER_BASE_IMAGE_TAG := beasleyweatherstation/base:armv7-1
DOCKER_BASE_IMAGE_TAG := beasleyweatherstation/server:armv7-1
DOCKER_BASE_IMAGE_TAG := beasleyweatherstation/station:armv7-1
DOCKER_BASE_IMAGE_TAG := beasleyweatherstation/transfer-client:armv7-1
```

The 'base' image is a REQUIREMENT FOR ALL OTHER IMAGES. If you, as in this example,
create a new version with the 'armv7-1' tag, you will need to, BEFORE building the other
images, update their respective `Dockerfile`s to ensure they're using the new 'base'
image instead of the default image. For this you need to edit the `FROM` command, `FROM
beasleyweatherstation/base:armv7-1`.

Then you need to run `make docker.build.base`, `make docker.build.transfer-client`, `make
docker.build.server`, `make docker.build.station` (you may only wish to build a subset if
you're only running the station and transfer-client on a ARM device). Building images
will require internet access as packages will be installed and any requisite images will
be pulled in from the Docker Hub repository. Building images will take a few minutes or
more depending on your connection and speed. Each images will download many hundreds of
megabytes from the internet so make sure to use a reliable internet connection.

The build images will be stored locally only (unless you decide to publish them to a
Docker repository like Docker Hub). See the Docker CLI reference for more information.

NOTE: Docker will build an image for whatever architecture you're building the image on.
So if you're building on a x86-64 laptop (Intel or AMD CPU), you're resulting image will
also be an x86-64 image. In order to build for an ARM CPU you will need to build on a ARM
device of the same version as your target platform architecture. There are ways of cross
compiling for different architectures, but this is not covered in this documentation.

### Review

- Verify the `docker-compose.yml` files are using the correct `image` values
- Verify the `Dockerfile` files are using the correct `FROM` images
- Make any changes to the `Makefile`'s `DOCKER_X_IMAGE_TAG` variables if you're building
  images locally
- Build images

## Running the Server

NOTE: Verify the `docker-compose.yml` files are using the correct `image` values for
you're particular platform and desired version. Remember, images are platform
architecture specific.

To run the Server, you will need to specify a port to run the Transfer System Server on.
The Docker compose file will run the Transfer System bound to the specified port on the
host's address. The Nginx server will be bound to the host's port 80.

    export DTS_PORT=24242

You can then call the Make target `up.serverd` to bring up the whole Server system.
Alternatively call `docker-compose` with the options manually (see the Makefile's
`up.serverd` target)

    make up.serverd

Please see the transfer-system/README.md for more configuration options.

## Running the Weather Station Client

To run the Weather Station Client, you will need to connect the Acurite to the host
system and export a environment variable specifying the for the address of the Server for
the Weather Station Client's Transfer System.

    export DTS_SERVER=127.0.0.1:24242

You can then call the Make target `up.stationd` to bring up the whole Weather Station
Client system.  Alternatively call `docker-compose` with the options manually (see the
Makefile's `up.stationd` target)

    make up.stationd

## Docker CLI Reference

Docker runs as a daemon. You interact with it using the `docker` command. Make sure the
daemon is running after it is installed (with System-D you need to run `sudo systemctl
start docker`). Docker requires Super User privileges by default, therefore you need to
prefix all commands with `sudo` or elevate your privileges using `sudo -i` to spawn a new
shell with Super User privileges beforehand.

### Useful Commands

#### General
- See what containers are running and their status: `docker ps`
- See all containers (running and stopped) and their status: `docker ps -a`
- Stop a container: `docker stop <CONTAINER_ID or NAME>`
- Remove a stopped container: `docker rm <CONTAINER_ID or NAME`
- Start a container: `docker run <IMAGE or IMAGE:TAG>`
- Execute a command on a running container: `docker exec <CONTAINER_ID OR NAME> <COMMAND>`
  - **This can be used to enter a shell on a running container: `docker exec -it <CONTAINER_ID OR NAME> bash`**
- You can access help using: `docker --help` or `docker <COMMAND> --help` or `man docker` or `man docker-<COMMAND>`

#### Images, Volumes and Networks
- See all locally stored images: `docker images`
- See all volumes: `docker volume ls`
- See all networks: `docker network ls`
- Remove a image: `docker rmi <NAME or IMAGE_ID>` or `docker image rm`
- Remove all unused images: `docker image prune`
- Volumes and networks have a similar interface to images, just replace `docker image` with `docker network` or `docker volume`

### Notes
- Docker images so take up a lot of space, so make sure to frequently inspect the local
  images and prune/remove any temporary (created by docker as temporary cache images to
  speed up rebuilds) and other unneeded images.
- Make sure to stop and remove any container not in used and or not required any more.
- The official Docker reference documentation is a very good resource for any questions
  you make have about how to do something: https://docs.docker.com/reference/
