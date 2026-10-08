from django.contrib.auth import get_user_model
from django.test import TestCase

from django.urls import reverse

from .models import Product


class ProductCrudTests(TestCase):
	def setUp(self):
		self.user = get_user_model().objects.create_user(username='admin', password='Testpass123!')
		self.client.force_login(self.user)
		self.product = Product.objects.create(
			name='Notebook',
			category='School Supplies',
			quantity=12,
			price='45.50',
			supplier='ABC Trading',
			status='Available',
		)

	def test_inventory_lists_products(self):
		response = self.client.get(reverse('product-list'))

		self.assertEqual(response.status_code, 200)
		self.assertContains(response, 'Notebook')

	def test_product_can_be_created(self):
		response = self.client.post(reverse('product-create'), {
			'name': 'Ballpen',
			'category': 'School Supplies',
			'quantity': 0,
			'price': '10.00',
			'supplier': 'XYZ Supply',
		})

		self.assertRedirects(response, reverse('product-list'))
		product = Product.objects.get(name='Ballpen')
		self.assertEqual(product.status, 'Out_of_stock')

	def test_product_can_be_updated(self):
		response = self.client.post(reverse('product-update', args=[self.product.product_id]), {
			'name': 'Large Notebook',
			'category': 'School Supplies',
			'quantity': 5,
			'price': '55.00',
			'supplier': 'ABC Trading',
		})

		self.assertRedirects(response, reverse('product-list'))
		self.product.refresh_from_db()
		self.assertEqual(self.product.name, 'Large Notebook')

	def test_product_can_be_deleted(self):
		response = self.client.post(reverse('product-delete', args=[self.product.product_id]))

		self.assertRedirects(response, reverse('product-list'))
		self.assertFalse(Product.objects.filter(product_id=self.product.product_id).exists())

	def test_product_code_is_generated_as_random_numeric_code(self):
		self.assertTrue(self.product.product_code.isdigit())
		self.assertEqual(len(self.product.product_code), 8)

	def test_inventory_can_be_searched(self):
		Product.objects.create(
			name='Marker Pen',
			category='Office Supplies',
			quantity=5,
			price='20.00',
			supplier='Office Depot',
			status='Available',
		)
		response = self.client.get(reverse('product-list'), {'q': 'Marker'})
		self.assertContains(response, 'Marker Pen')
		self.assertNotContains(response, 'Notebook')

	def test_anonymous_user_is_redirected_to_login(self):
		self.client.logout()
		response = self.client.get(reverse('product-list'))
		self.assertEqual(response.status_code, 302)
		self.assertIn('/accounts/login/', response.url)

	def test_account_can_be_created_and_used_to_log_in(self):
		self.client.logout()
		response = self.client.post(reverse('register'), {
			'username': 'newuser',
			'password1': 'ValidPass123!',
			'password2': 'ValidPass123!',
		})

		self.assertRedirects(response, reverse('login'))
		user = get_user_model().objects.get(username='newuser')
		self.assertTrue(user.check_password('ValidPass123!'))

		response = self.client.post(reverse('login'), {
			'username': 'newuser',
			'password': 'ValidPass123!',
		})
		self.assertRedirects(response, reverse('product-list'))

	def test_login_and_registration_pages_link_to_each_other(self):
		self.client.logout()
		login_response = self.client.get(reverse('login'))
		register_response = self.client.get(reverse('register'))

		self.assertContains(login_response, reverse('register'))
		self.assertContains(register_response, reverse('login'))

	def test_account_creation_rejects_mismatched_passwords(self):
		self.client.logout()
		response = self.client.post(reverse('register'), {
			'username': 'newuser',
			'password1': 'ValidPass123!',
			'password2': 'DifferentPass123!',
		})

		self.assertEqual(response.status_code, 200)
		self.assertFalse(get_user_model().objects.filter(username='newuser').exists())

	def test_negative_quantity_is_rejected(self):
		response = self.client.post(reverse('product-create'), {
			'name': 'Invalid Product',
			'category': 'Other',
			'quantity': -1,
			'price': '10.00',
			'supplier': 'Supplier',
		})

		self.assertEqual(response.status_code, 200)
		self.assertFalse(Product.objects.filter(name='Invalid Product').exists())
