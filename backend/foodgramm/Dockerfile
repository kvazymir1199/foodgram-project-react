FROM python:3.10.9-slim
WORKDIR /app

COPY requirements.txt .
RUN pip3 install -r /app/requirements.txt --no-cache-dir
COPY . .

CMD ["gunicorn", "foodgramm.wsgi:application", "--bind", "0:8000" ]
