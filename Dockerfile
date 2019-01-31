FROM python:3.6.6

RUN mkdir /app
COPY . /app

WORKDIR /app
RUN pip install -r requirements.txt
#RUN python manage.my migrate
RUN chmod +x start_backend.sh