FROM python:3.10-slim

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r deployment/requirements.txt

EXPOSE 8000

CMD ["gunicorn", "-c", "deployment/gunicorn_conf.py", "deployment.app:app"]
