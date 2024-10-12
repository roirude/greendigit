from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

from allauth.account.models import EmailAddress

from products.models import Product, Category, SubCategory

User = get_user_model()


class ProductTests(TestCase):
    def setUp(self):
        self.group, created = Group.objects.get_or_create(name='Farmers')
        self.farmer = User.objects.create_user(
            email='farmer@test.com',
            password='securepwd',
            is_farmer=True
        )
        self.farmer.groups.add(self.group)
        EmailAddress.objects.create(user=self.farmer, email=self.farmer.email, verified=True, primary=True)
        
        self.category = Category.objects.create(
            name='New Category',
            description='A Category description',
        )
        
        self.sub_category = SubCategory.objects.create(
            name='New SubCategory',
            description='A SubCategory description',
            category=self.category
        )
        
        self.product_data = {
            'name': 'New Product',
            'description': 'A product description',
            'sub_category': self.sub_category.id,
            'quantity': 30,
            'price': 3000
        }
        
    def test_add_product_as_authenticated_farmer(self):
        self.client.login(email='farmer@test.com', password='securepwd')
        
        response = self.client.post(reverse('add_product'), self.product_data)
        if response.status_code == 200 and response.context and 'form' in response.context:
            print("Form errors:", response.context['form'].errors)

        self.assertTrue(self.farmer.is_authenticated)
        self.assertTrue(self.farmer.groups.filter(name='Farmers').exists())
        
        self.assertEqual(response.status_code, 302)
        
        product = Product.objects.get(name='New Product')
        self.assertEqual(product.name, self.product_data['name'])