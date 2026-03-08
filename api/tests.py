from rest_framework.test import APITestCase
from .models import User,Order,Product
from django.urls import reverse



class ProductAPITestCase(APITestCase):
    def setUp(self):
        self.admin_user=User.objects.create_superuser(username="admin_test",password="pass123")
        self.normal_user=User.objects.create_user(username="user_test",password="pass123")
        self.product=Product.objects.create(
            name="air fryer",
            description="a cooking machine used to build bodies basically",
            price=15.04,
            stock=3,

        )
        self.url=reverse('product_detail',kwargs={'product_id':self.product.pk})


    # def test_product_detail(self):
    #     response=self.client.get(self.url)
    #     self.assertEqual(response.status_code,200)
    #     self.assertEqual(response.data['name'],self.product.name)


    # def test_unauthorized_access(self):
    #     data={"name":"updated product"}
    #     response=self.client.put(self.url,data)
    #     self.assertEqual(response.status_code,401)


    def test_authorization(self):
        # self.client.login(username="user_test",password="pass123")
        # response=self.client.delete(self.url)
        # self.assertEqual(response.status_code,403)
        # self.assertTrue(Product.objects.filter(pk=self.product.pk).exists())

        self.client.login(username="admin_test",password="pass123")
        response=self.client.delete(self.url)
        self.assertEqual(response.status_code,204)
        self.assertFalse(Product.objects.filter(pk=self.product.pk).exists())



