from django.test import RequestFactory, TestCase
from django.shortcuts import reverse
from django.contrib.auth.models import User
from shop.models import Category, Product
from shop.views import product_list, product_detail


class ShopViewsTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.category = Category.objects.create(name='Test Category', slug='test-category')
        self.product = Product.objects.create(
            category=self.category,
            name='Test Product',
            slug='test-product',
            price=10.99,
            available=True
        )

    def test_product_list_view(self):
        request = self.factory.get(reverse('shop:product_list'))
        response = product_list(request)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'shop/product/list.html')
        self.assertEqual(response.context['category'], None)
        self.assertQuerysetEqual(response.context['categories'], ['<Category: Test Category>'])
        self.assertQuerysetEqual(response.context['products'], ['<Product: Test Product>'])

    def test_product_list_view_with_category(self):
        request = self.factory.get(reverse('shop:product_list_by_category', args=['test-category']))
        response = product_list(request, category_slug='test-category')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'shop/product/list.html')
        self.assertEqual(response.context['category'], self.category)
        self.assertQuerysetEqual(response.context['categories'], ['<Category: Test Category>'])
        self.assertQuerysetEqual(response.context['products'], ['<Product: Test Product>'])

    def test_product_detail_view(self):
        request = self.factory.get(reverse('shop:product_detail', args=[self.product.id, 'test-product']))
        response = product_detail(request, id=self.product.id, slug='test-product')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'shop/product/detail.html')
        self.assertEqual(response.context['product'], self.product)
        self.assertEqual(response.context['cart_product_form'].initial, {'quantity': 1})
        self.assertEqual(len(response.context['recommended_products']), 0)

