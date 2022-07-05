
from django.core.management.base import BaseCommand
from django.core.mail import send_mail



class Command(BaseCommand):
    def handle(self, *args, **options):
        send_mail('test','Hello' , None,['sahiltiwariofficial10@gmail.com'])