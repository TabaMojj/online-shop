import datetime
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from coupons.models import Coupon


class CouponApplyTest(TestCase):
    def setUp(self):
        self.url = reverse('cart:coupon_apply')
        self.valid_coupon = Coupon.objects.create(
            code='TEST123',
            valid_from=timezone.now() - datetime.timedelta(days=1),
            valid_to=timezone.now() + datetime.timedelta(days=1),
            active=True
        )
        self.invalid_coupon = Coupon.objects.create(
            code='INVALID',
            valid_from=timezone.now() + datetime.timedelta(days=1),
            valid_to=timezone.now() + datetime.timedelta(days=2),
            active=True
        )

    def test_coupon_apply_valid(self):
        data = {'code': 'TEST123'}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('cart:cart_detail'))
        self.assertEqual(self.client.session['coupon_id'], self.valid_coupon.id)

    def test_coupon_apply_invalid(self):
        data = {'code': 'INVALID'}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('cart:cart_detail'))
        self.assertIsNone(self.client.session.get('coupon_id'))

    def test_coupon_apply_form_invalid(self):
        data = {'code': ''}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('cart:cart_detail'))
        self.assertIsNone(self.client.session.get('coupon_id'))
