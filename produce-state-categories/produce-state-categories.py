import pika

queue_name = 'events-v1'

# def send_message(message, queue_name=queue_name):
connection = pika.BlockingConnection(pika.ConnectionParameters('queue'))
channel = connection.channel()

channel.basic_publish(exchange='', routing_key=queue_name, body="james test")

connection.close()
