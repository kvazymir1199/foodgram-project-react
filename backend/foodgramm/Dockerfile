FROM python:3.10.9-slim
RUN mkdir /app

COPY requirements.txt/ /app
RUN pip3 install -r /app/requirements.txt --no-cache-dir
COPY . /app
# # COPY backend/foodgramm/ ./

WORKDIR /app
CMD ["gunicorn", "foodgramm.wsgi:application", "--bind", "0:8000" ]
