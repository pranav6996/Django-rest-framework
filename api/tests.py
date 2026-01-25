from django.test import TestCase
from .models import User,Order
from django.urls import reverse
from rest_framework import status

# Create your tests here.

class UserOrderTestCase(TestCase):
    def setUp(self):
        user1=User.objects.create_user(username='user1',password='pass123')
        user2=User.objects.create_user(username='user2',password='pass123')
        Order.objects.create(user=user1)
        Order.objects.create(user=user1)
        Order.objects.create(user=user2)
        Order.objects.create(user=user2)

    def test_user_order_endpoint_retrieves_only_authenticated_user_orders(self):
            user=User.objects.get(username='user1')
            self.client.force_login(user)
            response=self.client.get(reverse('user-orders'))

            assert response.status_code == 200
            orders=response.json()
            self.assertTrue(all(order['user']==user.id for order in orders))  # this checks if the data we got is assocaited with that user data only and all the orders that were displayed as json is by the same user's orders or not

    def test_user_order_list_unauthenticated(self):
         response=self.client.get(reverse('user-orders'))
         self.assertEqual(response.status_code,403)      






