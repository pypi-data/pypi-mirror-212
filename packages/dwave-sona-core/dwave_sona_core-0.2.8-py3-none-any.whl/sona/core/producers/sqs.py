import boto3

from .base import ProducerBase


class SQSProducer(ProducerBase):
    def __init__(self):
        self.sqs = boto3.resource("sqs")

    def emit(self, topic, message):
        queue = self.sqs.get_queue_by_name(QueueName=topic)
        queue.send_message(MessageBody=message)
