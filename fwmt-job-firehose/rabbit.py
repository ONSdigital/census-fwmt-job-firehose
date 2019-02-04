import pika

def init_app(app):
    pass

class RabbitProxy:
    def __init__(self):
        self.connection = pika.BlockingConnection()
        self.channel = self.connection.channel()
        self.channel.confirm_delivery()
        self.properties = pika.BasicProperties(content_type = 'text/json', delivery_mode = 1)

    def send(self, msg):
        return self.channel.basic_publish(
            exchange    = '',
            routing_key = 'Action.Field',
            body        = msg,
            properties  = self.properties)

    def close(self):
        self.connection.close()

