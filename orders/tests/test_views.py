from django.contrib.sessions.backends.cache import SessionStore
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from orders.models import Order, OrderItem, Product
from cart.cart import Cart


class OrderCreateViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.product = Product(product_id=1, price=10, quantity=2)
        self.cart = Cart(self._get_request())
        self.cart.add(self.product)

    def _get_request(self):
        request = self.client.request().wsgi_request
        request.session = SessionStore()
        return request

    def test_order_create_view_with_valid_form(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(reverse('order:create'), {
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'email': 'test@example.com',
            'address': 'address',
            'postal_code': '12345',
            'city': 'City',
        })
        self.assertEqual(response.status_code, 302)  # Should redirect to payment:process
        self.assertEqual(Order.objects.count(), 1)
        self.assertEqual(OrderItem.objects.count(), 1)
        self.assertEqual(len(self.cart), 0)  # Cart should be cleared

    def test_order_create_view_with_invalid_form(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(reverse('order:create'), {})
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'first_name', 'This field is required')


class AdminOrderDetailViewTest(TestCase):
    def setUp(self):
        self.admin_user = User.objects.create_superuser(username='admin', password='adminpassword')
        self.order = Order.objects.create(first_name='First Name', last_name='Last Name', email='test@example.com',
                                          address='address', postal_code='12345', city='City')

    def test_admin_order_detail_view(self):
        self.client.login(username='admin', password='adminpassword')
        response = self.client.get(reverse('order:admin_order_detail', args=[self.order.id]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['order'], self.order)


class AdminOrderPDFViewTest(TestCase):
    def setUp(self):
        self.admin_user = User.objects.create_superuser(username='admin', password='adminpassword')
        self.order = Order.objects.create(first_name='First Name', last_name='Last Name', email='test@example.com',
                                          address='123 Main St', postal_code='12345', city='City')

    def test_admin_order_pdf_view(self):
        self.client.login(username='admin', password='adminpassword')
        response = self.client.get(reverse('order:admin_order_pdf', args=[self.order.id]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/pdf')
        self.assertEqual(response['Content-Disposition'], f'filename=order_{self.order.id}.pdf')
