import pika
from models import Model
from faker import Faker

credentials = pika.PlainCredentials('guest', 'guest')
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))
channel = connection.channel()

channel.exchange_declare(exchange='email_service', exchange_type='direct')
channel.queue_declare(queue='email_send', durable=True)
channel.queue_bind(exchange='email_service', queue='email_send')


def main():
    for i in range(10):
        mail = Model(fullname=Faker().name(),
                     email=Faker().ascii_free_email()).save()

        channel.basic_publish(
            exchange='email_service',
            routing_key='email_send',
            body=str(mail.id).encode(),
            properties=pika.BasicProperties(
                delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
            ))
    connection.close()


if __name__ == '__main__':
    main()
