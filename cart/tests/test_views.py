from django.test import TestCase, Client
from django.urls import reverse
from shop.models import Product
from cart.cart import Cart


class CartAddTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.product = Product.objects.create(name='Test Product', price=10.0)
        self.cart_add_url = reverse('cart:cart_add', args=[self.product.id])

    def test_cart_add_positive(self):
        response = self.client.post(self.cart_add_url, {'quantity': 1, 'override': False})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(len(Cart(self.client.session)), 1)

    def test_cart_add_negative(self):
        response = self.client.post(self.cart_add_url, {'quantity': -1, 'override': False})
        self.assertEqual(response.status_code, 404)
        self.assertEqual(len(Cart(self.client.session)), 0)


class CartRemoveTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.product = Product.objects.create(name='Test Product', price=10.0)
        self.cart = Cart(self.client.session)
        self.cart.add(product=self.product, quantity=1, override_quantity=False)
        self.cart_remove_url = reverse('cart:cart_remove', args=[self.product.id])

    def test_cart_remove_positive(self):
        response = self.client.post(self.cart_remove_url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(len(self.cart), 0)

    def test_cart_remove_negative(self):
        response = self.client.post(self.cart_remove_url)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(len(self.cart), 1)


class CartDetailTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.cart_detail_url = reverse('cart:cart_detail')

    def test_cart_detail_positive(self):
        response = self.client.get(self.cart_detail_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cart/detail.html')

    def test_cart_detail_negative(self):
        response = self.client.get(self.cart_detail_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cart/detail.html')
        self.assertQuerysetEqual(response.context['recommended_products'], [])

        product = Product.objects.create(name='Test Product', price=10.0)
        cart = Cart(self.client.session)
        cart.add(product=product, quantity=1, override_quantity=False)
        response = self.client.get(self.cart_detail_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cart/detail.html')
        self.assertQuerysetEqual(response.context['recommended_products'], [])
