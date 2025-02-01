#!/bin/bash
# SI los contenedores estan creados primero los elimino y despues los vuelvo a crear
docker rm -f demo-mail
docker rm -f demo-rabbitmq
# Activando mi entorno virtual.
# source venv/bin/activate

# docker network create demonetwork
# Start Mailhog
# docker run --network= --name demo-mail -d mailhog/mailhog
# docker run --network=demonetwork --name demo-mail -p 8025:8025 -d mailhog/mailhog
docker run -d --rm --name demo-mail -p 8025:8025 -p  1025:1025 -d mailhog/mailhog
# Start RabbitMQ
# docker run -d --rm --name demo-rabbitmq -p 5672:5672 -d rabbitmq:3
# user default = guest and passwork default = guest
docker run -d --rm --name demo-rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:3-management
# docker run --network=demonetwork --name demo-rabbitmq -d rabbitmq:3
echo "Esperando el inicio de rabbitmq ..." && sleep 20
# Start Celery Worker
# cd src/
# celery -A demo worker -l info -B --scheduler django_celery_beat.schedulers:DatabaseScheduler
celery -A demo worker -l info -B
# --scheduler django_celery_beat.schedulers:DatabaseScheduler
# Clean containers at the end (optional)
# cd ../
# docker rm -f demo-mail
# docker rm -f demo-rabbitmq