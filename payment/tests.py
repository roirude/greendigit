from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib.messages import get_messages

from allauth.account.models import EmailAddress

from payment.models import Transaction, Receipt
from products.models import Product, Category, SubCategory
from users.models import Consumer, Farmer

User = get_user_model()

class PaiementTest(TestCase):
    def setUp(self):
        self.group, created = Group.objects.get_or_create(name='Farmers')
        self.group_consumer, created_csmr = Group.objects.get_or_create(name='Consumers')
        self.farmer = User.objects.create_user(
            email='farmer@test.com',
            password='securepwd',
            is_farmer=True
        )
        self.farmer.groups.add(self.group)
        EmailAddress.objects.create(user=self.farmer, email=self.farmer.email, verified=True, primary=True)
        Farmer.objects.create(user=self.farmer)
        
        self.category = Category.objects.create(
            name='New Category',
            description='A Category description',
        )
        
        self.sub_category = SubCategory.objects.create(
            name='New SubCategory',
            description='A SubCategory description',
            category=self.category
        )
        
        self.product = Product.objects.create(
            name='New Product',
            description='A product description',
            sub_category=self.sub_category,
            quantity=10,
            price=100,
            farmer=self.farmer,
        )
        
        
        self.consumer = User.objects.create_user(
            email='consumer@test.com',
            password='securepwd',
            is_consumer=True
        )
        self.consumer.groups.add(self.group_consumer)
        Consumer.objects.create(user=self.consumer)
        
        self.order_url = reverse('checkout_payment', kwargs={'slug': self.product.slug})
    
    def test_successful_order_as_authenticated_consumer(self):
        self.client.login(email='consumer@test.com', password='securepwd')

        response = self.client.post(self.order_url, {
            'product_quantity': 2,
            'payment_number': '237400001019'
        })

        self.assertEqual(response.status_code, 302)

        transaction = Transaction.objects.last()
        self.assertIsNotNone(transaction)
        self.assertEqual(transaction.product, self.product)
        self.assertEqual(transaction.consumer, self.consumer)
        self.assertEqual(transaction.amount, 200.00)

        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any("Payment successfully completed" in str(message) for message in messages))
        
        