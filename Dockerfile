# syntax=docker/dockerfile:1

ARG PYTHON_VERSION=3.12.5
FROM python:${PYTHON_VERSION}-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

ARG UID=10001
RUN adduser \
    --disabled-password \
    --gecos "" \
    --home "/nonexistent" \
    --shell "/sbin/nologin" \
    --no-create-home \
    --uid "${UID}" \
    tikhon

COPY requirements.txt .
RUN --mount=type=cache,target=/root/.cache/pip \
    --mount=type=bind,source=requirements.txt,target=requirements.txt \
    python -m pip install -r requirements.txt


FROM base AS dev
COPY . .
RUN python manage.py makemigrations --noinput --settings=voximplant_medsenger_bot.settings.development \
    && python manage.py migrate --noinput --settings=voximplant_medsenger_bot.settings.development
USER tikhon
EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000", "--settings=voximplant_medsenger_bot.settings.development"]


FROM base AS prod
COPY . .
RUN python manage.py collectstatic --noinput --settings=voximplant_medsenger_bot.settings.production
USER tikhon
CMD ["gunicorn", "--bind", "0.0.0.0:3045", "--access-logfile", "-", "-w", "2", "voximplant_medsenger_bot.wsgi:application"]


FROM base AS worker
RUN apt update && apt install -y cron
RUN touch /var/log/cron.log
RUN (crontab -l ; echo " * * * * * /usr/local/bin/python /app/manage.py start_background_worker --one-shot > /proc/1/fd/1 2>/proc/1/fd/2\n") | crontab
COPY . .
CMD ["./worker_entrypoint.sh"]
