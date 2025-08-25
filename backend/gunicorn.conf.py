bind = "0.0.0.0:5000"
workers = 1               # eventlet runs many green threads in a single worker
worker_class = "eventlet"
threads = 1
preload_app = False
daemon = False
