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

## Running the Server

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
