#!/bin/sh

if [ "$PROJECT_SERVICE_TYPE" = "api" ];
 then
  echo ">>> Run Migration"
  python manage.py migrate -v 0
  echo ">>> Collect Static Files"
  python manage.py collectstatic --noinput -v 0
  echo ">>> Starting Gunicorn"
  gunicorn core.asgi core.tools.uvicorn.NoLifespanUvicornWorker
fi
