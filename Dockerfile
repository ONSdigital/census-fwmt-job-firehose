FROM python:3-stretch
ADD app.py config.py addresses/combined.json startup.sh ./
RUN pip install flask pika
EXPOSE 5000
VOLUME ["/firehose-data"]
ENTRYPOINT ["entrypoint.sh"]
CMD ["flask", "init-db"]
