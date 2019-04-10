FROM python:3-alpine

ARG secret
ARG rabbit_url="rabbitmq"
ARG rabbit_user="guest"
ARG rabbit_pass="guest"

VOLUME ["/firehose-data"]
COPY ./fwmt-job-firehose /fwmt-job-firehose
COPY ./data /data
COPY requirements.txt /
RUN mkdir /instance

ENV FLASK_APP=fwmt-job-firehose

RUN echo "SECRET_KEY = '${secret}'" >> /instance/config.py
RUN echo "RABBIT_URL = '${rabbit_url}'" >> /instance/config.py
RUN echo "RABBIT_USERNAME = '${rabbit_user}'" >> /instance/config.py
RUN echo "RABBIT_PASSWORD = '${rabbit_pass}'" >> /instance/config.py

RUN pip install -r requirements.txt

RUN flask init-db

RUN flask load-address-json "/data/addresses_east.json"
RUN flask load-address-json "/data/addresses_south.json"
RUN flask load-address-json "/data/postcode_only_east.json"
RUN flask load-address-json "/data/postcode_only_southeast.json"
RUN flask load-address-json "/data/postcode_only_west.json"
RUN flask load-address-json "/data/addresses_north.json"
RUN flask load-address-json "/data/addresses_west.json"
RUN flask load-address-json "/data/postcode_only_south.json"
RUN flask load-address-json "/data/postcode_only_southwest.json"

EXPOSE 5000
ENTRYPOINT ["flask"]
CMD ["run", "-h", "0.0.0.0"]
