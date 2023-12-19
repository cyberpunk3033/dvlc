FROM python:3.10

#set envionment variables
ENV PYTHONUNBUFFERED 1

# run this before copying requirements for cache efficiency
RUN pip install --upgrade pip

#set work directory early so remaining paths can be relative
WORKDIR /data

# Adding requirements file to current directory
# just this file first to cache the pip install step when code changes
COPY requirements.txt .

#install dependencies
RUN pip install -r ./requirements.txt

# copy code itself from context to image
COPY . .
# run from working directory, and separate args in the json syntax
CMD ["python", "./manage.py", "runserver", "0.0.0.0:8000"]

#FROM ubuntu:latest
#RUN apt update && apt install -y nginx
#CMD nginx -g 'daemon off;'

