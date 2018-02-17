import pika
import json
import uuid
from elasticsearch import Elasticsearch

STORE_QUEUE_NAME = 'store'
QUEUE_HOSTNAME = 'queue'

connection = pika.BlockingConnection(pika.ConnectionParameters(QUEUE_HOSTNAME))
channel = connection.channel()

es = Elasticsearch(['elasticsearch'])


def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)
    data = json.loads(body)
    doc_type = data.pop('_type', 'unknown')
    id = data.pop('_id', uuid.uuid4())
    res = es.create(index='chamber-of-commerce', doc_type=doc_type, id=id, body=data)


channel.basic_consume(callback, queue=STORE_QUEUE_NAME, no_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')

channel.start_consuming()
