import random
from decimal import Decimal

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import lorem_ipsum
from api.models import User, Product, Order, OrderItem

class Command(BaseCommand):
    help = 'Creates application data'

    def handle(self, *args, **kwargs):
        # get or create superuser
        user = User.objects.filter(username='admin').first()
        if not user:
            user = User.objects.create_superuser(username='admin', password='test')

        # create products - name, desc, price, stock, image
        products = [
                     Product(name="A Scanner Darkly", description=lorem_ipsum.paragraph(), price=Decimal('12.99'), stock=4),
                     Product(name="Coffee Machine", description=lorem_ipsum.paragraph(), price=Decimal('70.99'), stock=6),
                     Product(name="Velvet Underground & Nico", description=lorem_ipsum.paragraph(), price=Decimal('15.99'), stock=11),
                     Product(name="Enter the Wu-Tang (36 Chambers)", description=lorem_ipsum.paragraph(), price=Decimal('17.99'), stock=2),
                     Product(name="Digital Camera", description=lorem_ipsum.paragraph(), price=Decimal('350.99'), stock=4),
                     Product(name="Luxury Watch", description=lorem_ipsum.paragraph(), price=Decimal('500.05'), stock=3),
                 
                     Product(name="Mechanical Keyboard", description=lorem_ipsum.paragraph(), price=Decimal('120.00'), stock=15),
                     Product(name="Gaming Mouse", description=lorem_ipsum.paragraph(), price=Decimal('49.99'), stock=25),
                     Product(name="4K Monitor", description=lorem_ipsum.paragraph(), price=Decimal('399.99'), stock=7),
                     Product(name="Bluetooth Speaker", description=lorem_ipsum.paragraph(), price=Decimal('89.99'), stock=12),
                     Product(name="Wireless Earbuds", description=lorem_ipsum.paragraph(), price=Decimal('149.99'), stock=18),
                     Product(name="Smartphone Stand", description=lorem_ipsum.paragraph(), price=Decimal('19.99'), stock=50),
                 
                     Product(name="Notebook Journal", description=lorem_ipsum.paragraph(), price=Decimal('9.99'), stock=100),
                     Product(name="Desk Lamp", description=lorem_ipsum.paragraph(), price=Decimal('39.99'), stock=22),
                     Product(name="Office Chair", description=lorem_ipsum.paragraph(), price=Decimal('199.99'), stock=5),
                     Product(name="Standing Desk", description=lorem_ipsum.paragraph(), price=Decimal('499.99'), stock=2),
                     Product(name="External Hard Drive", description=lorem_ipsum.paragraph(), price=Decimal('89.00'), stock=14),
                     Product(name="USB-C Hub", description=lorem_ipsum.paragraph(), price=Decimal('45.00'), stock=30),
                 
                     Product(name="Graphic Tablet", description=lorem_ipsum.paragraph(), price=Decimal('250.00'), stock=8),
                     Product(name="DSLR Camera", description=lorem_ipsum.paragraph(), price=Decimal('899.99'), stock=3),
                     Product(name="Tripod Stand", description=lorem_ipsum.paragraph(), price=Decimal('59.99'), stock=20),
                     Product(name="Noise Cancelling Headphones", description=lorem_ipsum.paragraph(), price=Decimal('299.99'), stock=6),
                     Product(name="Portable SSD", description=lorem_ipsum.paragraph(), price=Decimal('179.99'), stock=16),
                     Product(name="Action Camera", description=lorem_ipsum.paragraph(), price=Decimal('249.99'), stock=9),
                 
                     Product(name="Fitness Tracker", description=lorem_ipsum.paragraph(), price=Decimal('129.99'), stock=13),
                     Product(name="Smart LED Light", description=lorem_ipsum.paragraph(), price=Decimal('29.99'), stock=40),
                     Product(name="Electric Kettle", description=lorem_ipsum.paragraph(), price=Decimal('34.99'), stock=21),
                     Product(name="Backpack", description=lorem_ipsum.paragraph(), price=Decimal('79.99'), stock=17),
                     Product(name="Power Bank", description=lorem_ipsum.paragraph(), price=Decimal('39.99'), stock=35),
                     Product(name="Tablet Device", description=lorem_ipsum.paragraph(), price=Decimal('329.99'), stock=10),
    ]

        # create products & re-fetch from DB
        Product.objects.bulk_create(products)
        products = Product.objects.all()


        # create some dummy orders tied to the superuser
        for _ in range(3):
            # create an Order with 2 order items
            order = Order.objects.create(user=user)
            for product in random.sample(list(products), 2):
                OrderItem.objects.create(
                    order=order, product=product, quantity=random.randint(1,3)
                )