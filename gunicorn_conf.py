import os
import multiprocessing
bind = "127.0.0.1:8000"
workers = multiprocessing.cpu_count() * 2 + 1
chdir = os.path.abspath(os.path.dirname(__file__))
wsgi_app = "rendez_vous.wsgi:application"
accesslog = os.path.join(chdir, "logs/access.log")
errorlog = os.path.join(chdir, "logs/error.log")