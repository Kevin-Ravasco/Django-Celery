# Django Celery Integration & Running Background Tasks
This is a simple project to illustrate running background tasks in django using celery.

#### Features
- Running background tasks in django
- Scheduling tasks to run periodically (at certain times, certain days, certain itervals or in solar schedules)
- Scheduling periodic tasks from django admin
- Storing results of tasks in django database
- Using Redis and RabbitMQ as brokers in django

## Notes on Running Background Tasks

Installing the required packages:

`pip install celery`
`pip install django`
`pip install eventlet`

**NOTE:** Eventlet helped as tasks were being received by celery but
were not being executed by workers

Add the following to settings.py file:
```
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TASK_SERIALIZER = 'json'
CELERY_TIMEZONE = "Africa/Nairobi"
```

If using redis broker locally set CELERY_BROKER_URL as:
```
CELERY_BROKER_URL = 'redis://127.0.0.1:6379/'
```

If using rabbitmq use:

```
CELERY_BROKER_URL = 'amqp://localhost'
```

### Celery django setup:
Assuming our project is called 'core'. We create a `celery.py` file in the project root and
add the following code in the file:

These settings can be found in the 
[celery django integration documentation](https://docs.celeryq.dev/en/stable/django/first-steps-with-django.html)
```
import os

from celery import Celery

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

app = Celery('core')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
```

**NOTE**: Note the use of `core` in the code above, as our project is called core.

In the project root's `__init__.py` file, add:

```
# This will make sure the app is always imported when
# Django starts so that shared_task will use this app.
from .celery import app as celery_app

__all__ = ('celery_app',)
```

### Creating Tasks 
In `[app_name]/tasks.py` we can create tasks in the following way:
We make use of the shared_task decorator to create tasks.

```
from celery import shared_task

@shared_task
def verify_processed_emails() -> str:
    # execute something here
    return 'Emails verified successfully!'
    
```

In our views (or anywhere we need to call the task) we can run it by
calling the task using .delay() function. We can pass the parameters 
inside the delay function e.g. `my_addition_task.delay(5, 10)`. For
the case of our    `verify_processed_emails` task function, we can
call it as:

`verify_processed_emails.delay()`

#### Running Scheduled Tasks

We can run scheduled tasks in celery by using crontabs. The list of
scheduling can be found in 
[crontab schedules](https://docs.celeryq.dev/en/stable/userguide/periodic-tasks.html#crontab-schedules)

we install the requirements: `pip install django-celery-beat`

add to installed apps:

```
INSTALLED_APPS = (
    ...,
    'django_celery_beat',
)
```

Run migrations:

`python manage.py migrate`


Sample task code:

```
@shared_task
def test_scheduled_task(arg: str) -> str:
    """
    We use this as a test task for celery scheduling
    :param arg:
    :return: str
    """
    print(arg)
```
Notice the task above is the same as other tasks we defined earlier.
To be able to run it periodically, we take advantage of the django_celery_beat 
features. Visit the django admin and you can see the 'periodic tasks' app has 
a number of model entires such as 'clocked', 'crontabs', 'intervals', 'periodic tasks' 
and 'solar events'. We can schedule our tasks using the admin panel and selecting
the task we would like to run. We can add additional information such as description,
args and kwargs.

Start the **celery beat** service using the django_celery_beat.schedulers:DatabaseScheduler scheduler:

`celery -A proj beat -l INFO --scheduler django_celery_beat.schedulers:DatabaseScheduler`


####To store the results in the django database:
`pip install django-celery-results`

add the following line to settings.py:
```
CELERY_RESULT_BACKEND = 'django-db'
```


### Running Celery To Execute Tasks
To run celery in the console use this command

`celery -A myapp.celeryapp worker --loglevel=info -P eventlet`

For our case, our project called core has the celeryapp, we can run:

`celery -A core worker --loglevel=info -P eventlet`


##Additional Broker Notes
### Running Rabbitmq in windows
Open the rabbitmq cli

Server commands:

```shell
rabbitmq-service.bat stop  
rabbitmq-service.bat install  
rabbitmq-service.bat start  
```

To enable/disable the management:
```shell
rabbitmq-plugins.bat enable rabbitmq_management
rabbitmq-plugins.bat disable rabbitmq_management
```
When the management is enabled, visit [localhost link](http://localhost:15672/#/).
Login using the default username and password created by rabbit mq, username: guest, password: guest

