import pika

queue_name = 'events-v1'

connection = pika.BlockingConnection(pika.ConnectionParameters('queue'))
channel = connection.channel()


def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)


channel.basic_consume(callback, queue=queue_name, no_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')

channel.start_consuming()
