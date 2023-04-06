FROM python:3.9

ENV PYTHONUNBUFFERED 1

WORKDIR /EmergencyManagement

COPY requirements.txt /EmergencyManagement/
RUN pip install --index-url=https://www.piwheels.org/simple --no-cache-dir -r requirements.txt

COPY . /EmergencyManagement/

