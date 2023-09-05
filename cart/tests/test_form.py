from django import forms
from django.test import TestCase
from django.forms.fields import BooleanField

from cart.forms import CartAddProductForm


class CartAddProductFormTest(TestCase):
    def test_quantity_choices(self):
        form = CartAddProductForm()
        quantity_field = form.fields['quantity']
        self.assertEqual(quantity_field.choices, [(i, str(i)) for i in range(1, 21)])

    def test_quantity_coercion(self):
        form = CartAddProductForm(data={'quantity': '5'})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['quantity'], 5)

    def test_override_field(self):
        form = CartAddProductForm()
        override_field = form.fields['override']
        self.assertIsInstance(override_field, BooleanField)
        self.assertFalse(override_field.required)
        self.assertFalse(override_field.initial)

    def test_override_hidden_input(self):
        form = CartAddProductForm()
        override_field = form.fields['override']
        self.assertIsInstance(override_field.widget, forms.HiddenInput)

    def test_override_optional(self):
        form = CartAddProductForm(data={'quantity': '5'})
        self.assertTrue(form.is_valid())
        self.assertFalse(form.cleaned_data['override'])

    def test_override_checked(self):
        form = CartAddProductForm(data={'quantity': '5', 'override': 'on'})
        self.assertTrue(form.is_valid())
        self.assertTrue(form.cleaned_data['override'])
