from django.test import TestCase
from decimal import Decimal
from coupons.models import Coupon
from shop.models import Product
from orders.models import Order, OrderItem


class OrderModelTest(TestCase):
    def setUp(self):
        self.coupon = Coupon.objects.create(code='TESTCOUPON', discount=10)
        self.product = Product.objects.create(name='Test Product', price=Decimal('10.00'))
        self.order = Order.objects.create(first_name='John', last_name='Doe', email='john@example.com',
                                          address='123 Test St', postal_code='12345', city='Test City',
                                          coupon=self.coupon, discount=10)

    def test_get_total_cost_before_discount(self):
        order_item = OrderItem.objects.create(order=self.order, product=self.product, price=Decimal('10.00'),
                                              quantity=2)
        self.assertEqual(self.order.get_total_cost_before_discount(), Decimal('20.00'))

    def test_get_discount(self):
        self.assertEqual(self.order.get_discount(), Decimal('2.00'))

    def test_get_total_cost(self):
        self.assertEqual(self.order.get_total_cost(), Decimal('18.00'))

    def test_get_stripe_url(self):
        self.assertEqual(self.order.get_stripe_url(), '')

    def test_get_stripe_url_with_stripe_id(self):
        self.order.stripe_id = 'test_stripe_id'
        self.assertEqual(self.order.get_stripe_url(), 'https://dashboard.stripe.com/payments/test_stripe_id')


class OrderItemModelTest(TestCase):
    def setUp(self):
        self.product = Product.objects.create(name='Test Product', price=Decimal('10.00'))
        self.order = Order.objects.create(first_name='John', last_name='Doe', email='john@example.com',
                                          address='123 Test St', postal_code='12345', city='Test City')

    def test_get_cost(self):
        order_item = OrderItem.objects.create(order=self.order, product=self.product, price=Decimal('10.00'),
                                              quantity=2)
        self.assertEqual(order_item.get_cost(), Decimal('20.00'))
