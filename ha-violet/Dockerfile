# https://developers.home-assistant.io/docs/add-ons/configuration#add-on-dockerfile
ARG BUILD_FROM
#FROM $BUILD_FROM

FROM python:3.11-slim

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy root filesystem
COPY rootfs /

COPY . .

CMD [ "python", "./main.py" ]
