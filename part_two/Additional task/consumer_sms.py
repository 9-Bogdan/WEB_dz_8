import pika

from models import Model


credentials = pika.PlainCredentials('guest', 'guest')
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))
channel = connection.channel()

channel.queue_declare(queue='sms_send', durable=True)


def callback(ch, method, properties, body):
    pk = body.decode()
    sms = Model.objects(id=pk, boolean=False).first()
    if sms:
        sms.update(set__boolean=True)
        print(f"Sms updated {sms.id}")
    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='sms_send', on_message_callback=callback)


if __name__ == '__main__':
    channel.start_consuming()
