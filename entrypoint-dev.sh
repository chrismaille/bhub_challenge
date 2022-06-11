#!/bin/sh

echo ">>> Run Migration"
python manage.py migrate -v 0

if [ "$PROJECT_SERVICE_TYPE" = "api" ];
 then
  echo ">>> Starting Gunicorn"
  gunicorn core.asgi:application -k core.tools.uvicorn.NoLifespanUvicornWorker
fi

# Other services can run using the same docker image.
# A common pattern is to run API, Celery Worker and Beat containers
# That's the purpose of the PROJECT_SERVICE_TYPE environment variable.

#if [ "$PROJECT_SERVICE_TYPE" = "worker" ];
# then
#  echo ">>> Starting Celery Worker"
#  celery --app core worker --loglevel=INFO
#fi

#if [ "$PROJECT_SERVICE_TYPE" = "beat" ];
# then
#  echo ">>> Starting Celery Beat"
#  rm -f /tmp/celerybeat.pid
#  celery --app core beat --loglevel=INFO --pidfile /tmp/celerybeat.pid --scheduler django_celery_beat.schedulers:DatabaseScheduler
#fi

#if [ "$PROJECT_SERVICE_TYPE" = "flower" ];
# then
#  echo ">>> Starting Celery Flower"
#  celery --app core flower --address=0.0.0.0 --port=5555
#fi

echo ">>> No Service Configured. Running docker CMD if available..."
eval $@
