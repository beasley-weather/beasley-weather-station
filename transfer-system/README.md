## Running the transfer server

    DTS_PORT=1234 \
    WEEWX_DATABASE=weewx.sdb \
    python -m transfer_system.server

## Running the transfer client

    DTS_SERVER=254.254.254.254 \
    DTS_INTERVAL=300 \
    WEEWX_DATABASE=weewx.sdb
    python -m transfer_system.client
