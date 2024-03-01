#!/bin/bash

# Run migrations and collect static files
/app/src/migrate.sh
/app/src/collectstatic.sh

# Start Gunicorn
exec gunicorn order.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 3 \
    --max-requests 1200 \
    --limit-request-line 4094 \
    --limit-request-fields 100