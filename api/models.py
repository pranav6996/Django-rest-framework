from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid

class User(AbstractUser):  #abstract user to define the custom user model
    pass

class Product(models.Model):
    name=models.CharField(max_length=200)
    description=models.TextField()
    price=models.DecimalField(max_digits=10,decimal_places=2)
    stock=models.PositiveIntegerField()
    image=models.ImageField(upload_to='products/',blank=True,null=True)

    @property # this is used to perform calculations directly and return without storing them in the database and update the values dynamically based on th e current values
    
    def is_stock(self):
        return self.stock >0
    
    def __str__(self):
        return self.name
    

class Order(models.Model):
    class StatusChoices(models.TextChoices):
        PENDING='pending'
        COMPLETED='completed'
        CANCELLED='cancelled'
    
    order_id=models.TextField(primary_key=True,default=uuid.uuid4)
    user=models.ForeignKey(User,on_delete=models.CASCADE)  # this will delete all the data associated with the user
    created_at=models.DateTimeField(auto_now_add=True)
    status=models.CharField(max_length=10,choices=StatusChoices.choices,default=StatusChoices.PENDING)

    products=models.ManyToManyField(Product,through="OrderItem",related_item='orders')  # the first many to many fields is impplying that a product has many to many relations with other products too and the 2nd part of through ="OrderItem" is associated with how many quantity or
    #the number of items we are ordering for that product and the part related_item is used to make different queries to view the orders history of this specific product

    def __str__(self):
        return f'the order of id with id  {self.order_id} ordered by {self.user.username}'
    

