## Running the transfer server

    export DTS_PORT=1234
    export WEEWX_DATABASE=weewx.sdb # Optional (default /var/lib/weewx/weewx.sdb)
    python -m transfer_system.server

## Running the transfer client

    export DTS_SERVER=254.254.254.254
    export DTS_INTERVAL=300 # Optional (default 300)
    export WEEWX_DATABASE=weewx.sdb # Optional (default /var/lib/weewx/weewx.sdb)
    python -m transfer_system.client
