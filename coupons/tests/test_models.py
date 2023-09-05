from django.test import TestCase
from django.utils import timezone
from datetime import timedelta
from coupons.models import Coupon


class CouponTestCase(TestCase):
    def setUp(self):
        self.coupon = Coupon.objects.create(
            code='TESTCODE',
            valid_from=timezone.now(),
            valid_to=timezone.now() + timedelta(days=7),
            discount=50,
            active=True
        )

    def test_coupon_str(self):
        self.assertEqual(str(self.coupon), 'TESTCODE')

    def test_coupon_validity(self):
        self.assertTrue(self.coupon.valid_from < timezone.now() < self.coupon.valid_to)

    def test_coupon_discount_range(self):
        self.assertGreaterEqual(self.coupon.discount, 0)
        self.assertLessEqual(self.coupon.discount, 100)

    def test_coupon_active(self):
        self.assertTrue(self.coupon.active)

    def test_coupon_code_uniqueness(self):
        with self.assertRaises(Exception):
            Coupon.objects.create(
                code='TESTCODE',
                valid_from=timezone.now(),
                valid_to=timezone.now() + timedelta(days=7),
                discount=50,
                active=True
            )
