from celery import Celery

app = Celery('action_execution',
        broker='pyamqp://guest@ridlserver01//',
        backend='rpc://ridlserver01',
        include=['action_execution.tasks'])

if __name__ == '__main__':
    app.start()
