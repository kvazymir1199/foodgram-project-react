FROM python:3.10.9-slim
RUN mkdir /foodgramm

COPY requirements.txt/ /foodgramm
RUN pip3 install -r /foodgramm/requirements.txt --no-cache-dir
COPY . /foodgramm
# # COPY backend/foodgramm/ ./

WORKDIR /foodgramm
CMD ["gunicorn", "foodgramm.wsgi:application", "--bind", "0:8000" ]
