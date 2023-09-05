from decimal import Decimal
from django.test import TestCase
from django.contrib.sessions.backends.db import SessionStore
from coupons.models import Coupon
from shop.models import Product, Category
from cart.cart import Cart


class CartTestCase(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Test Category', slug='test-category')
        self.product = Product.objects.create(name='Test Product', price=10, category=self.category)
        self.cart = Cart(self._get_request())

    def _get_request(self):
        request = self.client.request().wsgi_request
        request.session = SessionStore()
        return request

    def test_add_product_to_cart(self):
        self.cart.add(self.product)
        self.assertEqual(len(self.cart), 1)
        self.assertEqual(self.cart.get_total_price(), Decimal(10))

    def test_add_product_with_quantity_to_cart(self):
        self.cart.add(self.product, quantity=2)
        self.assertEqual(len(self.cart), 2)
        self.assertEqual(self.cart.get_total_price(), Decimal(20))

    def test_update_product_quantity_in_cart(self):
        self.cart.add(self.product)
        self.cart.add(self.product, quantity=2, override_quantity=True)
        self.assertEqual(len(self.cart), 1)
        self.assertEqual(self.cart.get_total_price(), Decimal(20))

    def test_remove_product_from_cart(self):
        self.cart.add(self.product)
        self.cart.remove(self.product)
        self.assertEqual(len(self.cart), 0)
        self.assertEqual(self.cart.get_total_price(), Decimal(0))

    def test_get_total_price(self):
        self.cart.add(self.product)
        self.cart.add(self.product, quantity=2)
        self.assertEqual(self.cart.get_total_price(), Decimal(30))

    def test_clear_cart(self):
        self.cart.add(self.product)
        self.cart.clear()
        self.assertEqual(len(self.cart), 0)
        self.assertEqual(self.cart.get_total_price(), Decimal(0))

    def test_get_discount(self):
        coupon = Coupon.objects.create(code='TESTCODE', discount=10)
        self.cart.add(self.product)
        self.cart.coupon_id = coupon.id
        self.assertEqual(self.cart.get_discount(), Decimal(1))

    def test_get_total_price_after_discount(self):
        coupon = Coupon.objects.create(code='TESTCODE', discount=10)
        self.cart.add(self.product)
        self.cart.coupon_id = coupon.id
        self.assertEqual(self.cart.get_total_price_after_discount(), Decimal(9))

    def test_iterate_over_cart_items(self):
        self.cart.add(self.product)
        self.cart.add(self.product, quantity=2)
        items = list(self.cart)
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0]['product'], self.product)
        self.assertEqual(items[0]['quantity'], 3)
        self.assertEqual(items[0]['price'], Decimal(10))
        self.assertEqual(items[0]['total_price'], Decimal(30))

    def test_get_cart_length(self):
        self.cart.add(self.product)
        self.cart.add(self.product, quantity=2)
        self.assertEqual(len(self.cart), 3)
