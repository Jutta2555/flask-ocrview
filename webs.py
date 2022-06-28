app = Celery('tasks', backend='redis://localhost', broker='amqp://')
