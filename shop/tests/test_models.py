from django.urls import reverse
from django.test import TestCase
from shop.models import Category, Product


class CategoryTestCase(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Test Category', slug='test-category')

    def test_category_str(self):
        self.assertEqual(str(self.category), 'Test Category')

    def test_category_absolute_url(self):
        expected_url = reverse('shop:product_list_by_category', args=['test-category'])
        self.assertEqual(self.category.get_absolute_url(), expected_url)


class ProductTestCase(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Test Category', slug='test-category')
        self.product = Product.objects.create(
            category=self.category,
            name='Test Product',
            slug='test-product',
            price=10.99
        )

    def test_product_str(self):
        self.assertEqual(str(self.product), 'Test Product')

    def test_product_absolute_url(self):
        expected_url = reverse('shop:product_detail', args=[self.product.id, 'test-product'])
        self.assertEqual(self.product.get_absolute_url(), expected_url)

