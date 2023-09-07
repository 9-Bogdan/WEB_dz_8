import pika
from models import Model
from faker import Faker

credentials = pika.PlainCredentials('guest', 'guest')
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))
channel = connection.channel()


channel.exchange_declare(
    exchange='sms_or_email_service', exchange_type='topic')
channel.queue_declare(queue='email_send', durable=True)
channel.queue_bind(exchange='sms_or_email_service', queue='email_send')
channel.queue_declare(queue="sms_send", durable=True)
channel.queue_bind(exchange='sms_or_email_service', queue='sms_send')


def main():
    for i in range(10):
        email_or_sms = Faker().random_element(elements=["sms", "email"])
        if email_or_sms == "email":
            contact = Model(fullname=Faker().name(),
                            email=Faker().ascii_free_email(), phone=None, sms_or_email=email_or_sms).save()

            channel.basic_publish(
                exchange='', routing_key='email_send', body=str(contact.id))
        else:
            contact = Model(fullname=Faker().name(),
                            email=None, phone=Faker().phone_number(), sms_or_email=email_or_sms).save()

            channel.basic_publish(
                exchange='', routing_key='sms_send', body=str(contact.id))

    connection.close()


if __name__ == '__main__':
    main()
