from django.core.management.base import BaseCommand
from rabbitmq_management import Rabbitmq_Consumer_AuthUser
from queue import Queue


class Command(BaseCommand):
    help = "Start connection (consumer)"
    
    def handle(self, *args, **options):
        result_queue = Queue()
        self.stdout.write(self.style.SUCCESS("launch consumer2 successfuly"))
        while 1:
            Rabbitmq_Consumer_AuthUser(exchange_name='User', queue_name='get_order_user')
            received_message = result_queue.get()
            print(received_message)
            