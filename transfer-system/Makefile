run.client:
		python3 -m transfer_system.client

run.server:
		gunicorn --bind 0.0.0.0:$(DTS_PORT) transfer_system.server.__main__:app
		# python -m transfer_system.server
