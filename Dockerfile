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

COPY . .


FROM base AS dev
RUN python manage.py makemigrations --noinput --settings=voximplant_medsenger_bot.settings.development \
    && python manage.py migrate --noinput --settings=voximplant_medsenger_bot.settings.development
USER tikhon
EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000", "--settings=voximplant_medsenger_bot.settings.development"]


FROM base AS prod
RUN python manage.py collectstatic --noinput --settings=voximplant_medsenger_bot.settings.production
USER tikhon
EXPOSE 3045
CMD ["gunicorn", "--bind", "0.0.0.0:3045", "voximplant_medsenger_bot.wsgi"]


FROM base AS worker
USER tikhon
CMD ["python", "manage.py", "start_background_worker", "--settings=voximplant_medsenger_bot.settings.development"]
