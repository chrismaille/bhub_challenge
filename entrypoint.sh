#!/bin/sh

if [ "$PROJECT_SERVICE_TYPE" = "api" ];
 then
  echo ">>> Run Migration"
  python manage.py migrate -v 0
  echo ">>> Starting Gunicorn"
  gunicorn core.asgi:application -k core.tools.uvicorn.NoLifespanUvicornWorker
fi
